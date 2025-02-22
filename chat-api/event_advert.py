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
- **Strong Call to Action:** Encourage the listener to act now in a persuasive yet natural way.
- **No Redundant Phrases:** Keep it crisp and under fifty words.

Make the advertisement feel **energetic, smooth, and designed for spoken delivery** without awkward phrasing. 
"""
)

class LMNTtts:
    """Handles text-to-speech conversion using LMNT API."""

    def __init__(self, api_key: str, model: str = "blizzard", voice_id: str = "lily"):
        self.api_key = api_key
        self.voice_id = voice_id
        self.model = model

    async def synthesize(self, text: str) -> str:
        """Convert text to speech and save as an MP3 file."""
        async with Speech(self.api_key) as speech:
            synthesis = await speech.synthesize(text, self.voice_id, model=self.model)
        
        with open(output_audio_path, "wb") as f:
            f.write(synthesis["audio"])

        logger.success(f"Audio response saved to {output_audio_path}")
        return output_audio_path

async def generate_event_advert(event_data: dict):
    """Generate an advertisement from event data using the prompt correctly."""
    
    formatted_prompt = prompt.format(
        artist_name=event_data["artist_name"],
        event_type=event_data["event_type"],
        venue_name=event_data["venue_name"],
        city=event_data["city"],
        country=event_data["country"],
        event_start_date=event_data["event_start_date"],
        event_start_time=event_data["event_start_time"],
        genres=", ".join(event_data["genres"]),
        average_ticket_price=event_data["average_ticket_price"]
    )
    
    try:
        response = model.invoke(formatted_prompt)  # ✅ Correctly use the prompt
        advert_text = response.content  # ✅ Get the generated text
        logger.info(f"Generated advert: {advert_text}")

        # Convert text to speech
        tts = LMNTtts(api_key=lmnt_api_key)
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
