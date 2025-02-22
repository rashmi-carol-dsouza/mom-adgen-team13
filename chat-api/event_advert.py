import json
import os
from loguru import logger
from lmnt.api import Speech
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pydub import AudioSegment

load_dotenv()

# Configure logging
logger.add("logs/event_advert.log", rotation="1 MB", retention="10 days", level="INFO")

# Load API keys
mistral_api_key = os.getenv("MISTRAL_API_KEY")
lmnt_api_key = os.getenv("LMNT_API_KEY")

# Paths for data storage
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "../data")
os.makedirs(data_dir, exist_ok=True)
output_audio_path = os.path.join(data_dir, "advert.mp3")

# Initialize LLM Model
model = ChatMistralAI(mistral_api_key=mistral_api_key)

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
- **Smooth & Natural Flow:** Use conversational language that sounds like a real radio commercial.
- **Avoid Year Mentions:** The year is not needed unless absolutely necessary.
- **Strong Call to Action:** Encourage the listener to act now in a persuasive yet natural way. But there is no screen interactions.
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
        self.output_file = os.path.join(data_dir, "final_advert.mp3")

    async def synthesize(self, text: str) -> str:
        """Convert text to speech and save as an MP3 file."""
        async with Speech(self.api_key) as speech:
            synthesis = await speech.synthesize(text, self.voice_id, model=self.model)

        tts_audio_path = os.path.join(data_dir, "tts_output.mp3")
        
        with open(tts_audio_path, "wb") as f:
            f.write(synthesis["audio"])

        logger.success(f"TTS Audio saved to {tts_audio_path}")

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
            background = background - 10  # Reduce volume by 20 dB
            voice = voice + 1

            # Match lengths
            if len(background) < len(voice):
                background = background * (len(voice) // len(background) + 1)

            background = background[: len(voice)]  # Trim to fit voice length

            # Mix audio
            final_audio = voice.overlay(background)

            # Save final audio
            final_audio.export(self.output_file, format="mp3")
            logger.success(f"Final Advert saved to {self.output_file}")

            return self.output_file
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
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
        logger.info(f"Generated Advert Text: {advert_text}")

        # Background music file (replace with your actual music file path)
        bg_music_path = os.path.join(data_dir, "background_music.mp3")

        # Convert text to speech and add background music
        tts = LMNTtts(api_key=lmnt_api_key, bg_music_path=bg_music_path)
        mp3_file_path = await tts.synthesize(advert_text)

        return mp3_file_path
    except Exception as e:
        logger.error(f"Error generating advert: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating advert: {str(e)}")
    
# FastAPI setup
app = FastAPI()

ORIGIN_LOCAL_DEV = "http://localhost:5173"

class EventData(BaseModel):
    event: dict

@app.post("/generate-advert/")
async def generate_advert(event_data: EventData):
    try:
        mp3_file_path = await generate_event_advert(event_data.event)
        return FileResponse(mp3_file_path, media_type="audio/mpeg", filename="advert.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing advert request: {str(e)}")

@app.get("/")
def root():
    return {"message": "Welcome to the Event Advert API!"}
