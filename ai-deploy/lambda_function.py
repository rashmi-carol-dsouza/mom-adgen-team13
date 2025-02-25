import json
import os
import sys
import asyncio
import boto3
from pydub import AudioSegment
from lmnt.api import Speech
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# Ensure Lambda finds dependencies
sys.path.append("/var/task")

#  AWS S3 Configuration
S3_BUCKET_NAME = "event-advert-mp3-storage"  # Your S3 bucket name
S3_OUTPUT_FOLDER = "generated-audio/"  # Folder inside S3 for final adverts
BACKGROUND_MUSIC_KEY = "background.mp3"  # Background music stored in S3

#  Initialize AWS S3 client
s3_client = boto3.client("s3")

def get_lambda_env_variable(variable_name, function_name="event-advert-api", region="eu-central-1"):
    """Fetch environment variables dynamically from AWS Lambda configuration."""
    client = boto3.client("lambda", region_name=region)
    response = client.get_function_configuration(FunctionName=function_name)
    return response.get("Environment", {}).get("Variables", {}).get(variable_name, None)

mistral_api_key = get_lambda_env_variable("MISTRAL_API_KEY")
lmnt_api_key = get_lambda_env_variable("LMNT_API_KEY")
model = ChatMistralAI(mistral_api_key=mistral_api_key)

import random

random_number = random.randint(30, 50)
# Chat prompt template
prompt = ChatPromptTemplate.from_template(
    """
You are a professional voiceover assistant creating a short and engaging radio advertisement for a live music event. Your goal is to make the ad sound natural, exciting, and persuasive, just like a real radio commercial.

Event Details:
- Artist: {artist_name}
- Event: {event_type} at {venue_name}, {city}, {country}
- Date: {event_start_date} at {event_start_time} (use full words, avoid abbreviations)
- Genres: {genres}
- Do not mention ticket prices or currency.
- Convert numbers into words for better spoken delivery.

### **Guidelines for the Advertisement:**
- **Engaging Hook:** Start with an attention-grabbing line that excites the listener.
- **Did You Know Fact:** Mention that {random_number} people are already thinking about this event right now!
- **Smooth & Natural Flow:** Use conversational language that sounds like a real radio commercial.
- **Avoid Year Mentions:** The year is not needed unless absolutely necessary.
- **Strong Call to Action:** Persuade the listener to act now with a closing line like "Swipe up to book your tickets!"
- **No Redundant Phrases:** Keep it crisp and under fifty words.

Make the advertisement feel **energetic, smooth, and designed for spoken delivery** without awkward phrasing.  
"""
)

class LMNTtts:
   """Handles text-to-speech conversion and adds background music."""

   def __init__(self, api_key: str, model: str = "aurora", voice_id: str = "lily", bg_music_path: str = None):
       self.api_key = api_key
       self.voice_id = voice_id
       self.model = model
       self.bg_music_path = bg_music_path
       self.output_file = "/tmp/final_advert.mp3"  


   async def synthesize(self, text: str) -> str:
       """Convert text to speech and save as an MP3 file."""
       async with Speech(self.api_key) as speech:
           synthesis = await speech.synthesize(text, self.voice_id, model=self.model)


       tts_audio_path = "/tmp/tts_output.mp3"
       with open(tts_audio_path, "wb") as f:
           f.write(synthesis["audio"])


       print(f"TTS Audio saved to {tts_audio_path}")


       # If background music is provided, mix it with the TTS audio
       if self.bg_music_path:
           return self.mix_audio(tts_audio_path)
       else:
           return tts_audio_path


   def mix_audio(self, tts_audio_path: str) -> str:
       """Mix TTS audio with background music."""
       try:
           voice = AudioSegment.from_file(tts_audio_path)
           background = AudioSegment.from_file(self.bg_music_path).set_frame_rate(voice.frame_rate)


           # Lower background music volume
           background = background - 10  # Reduce volume
           voice = voice + 1  # Increase voice volume slightly


           # Match lengths
           if len(background) < len(voice):
               background = background * (len(voice) // len(background) + 1)


           background = background[: len(voice)]  # Trim to fit voice length


           # Mix audio
           final_audio = voice.overlay(background)


           # Save final audio
           final_audio.export(self.output_file, format="mp3")
           print(f"Final Advert saved to {self.output_file}")


           return self.output_file
       except Exception as e:
           print(f"Error mixing audio: {e}")
           return tts_audio_path  # Return the voice-only file if mixing fails


async def generate_event_advert(event_data: dict):
   """Generate an advertisement and add background music."""
  
   formatted_prompt = prompt.format(
       artist_name=event_data["artist_name"],
       event_type=event_data["event_type"],
       venue_name=event_data["venue_name"],
       city=event_data["city"],
       country=event_data["country"],
       event_start_date=event_data["event_start_date"],
       event_start_time=event_data["event_start_time"],
       genres=", ".join(event_data["genres"])
   )


   try:
       response = model.invoke(formatted_prompt) 
       advert_text = response.content.strip()
       print(f"Generated Advert Text: {advert_text}")


       # Background music file 
       bg_music_path = "event-advert-mp3-storage/background_music.mp3"


       # Convert text to speech and add background music
       tts = LMNTtts(api_key=lmnt_api_key, bg_music_path=bg_music_path)
       mp3_file_path = await tts.synthesize(advert_text)


       return mp3_file_path
   except Exception as e:
       print(f"Error generating advert: {e}")
       raise Exception(f"Error generating advert: {str(e)}")


def lambda_handler(event, context):
    """AWS Lambda handler function."""
    try:
        # Ensure body exists
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid request: 'body' field missing from event."})
            }
        
        # Parse request body
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON format in request body."})
            }

        event_data = body.get("event")
        if not event_data:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'event' field in request body."})
            }

        # Use asyncio event loop to call async function inside Lambda
        loop = asyncio.get_event_loop()
        mp3_file_path = loop.run_until_complete(generate_event_advert(event_data))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "audio/mpeg"},
            "body": mp3_file_path
        }

    except Exception as e:
        print(f"Lambda processing error: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }