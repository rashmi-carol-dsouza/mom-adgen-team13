import json
import os
from os import path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI
from lmnt.api import Speech
from pydantic import BaseModel
from pydub import AudioSegment


class UserInput(BaseModel):
    lon: str
    lat: str
    language: str | None
    genre: list[str]


import psycopg
import requests
from loguru import logger

db_name = "koyebdb"
db_user = "koyeb-adm"
db_password = "npg_4ABuiR8rKdwW"
db_host = "ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app"

event_by_genre_by_location_query = """
SELECT
    e.id AS event_id,
    e.start_date,
    e.event_type,
    e.start_time,
    e.average_ticket_price,
    e.fans_interested,
    e.fans_going,
    v.id AS venue_id,
    v.name AS venue_name,
    v.address,
    v.city,
    v.country,
    a.id AS artist_id,
    a.name AS artist_name,
    g.name AS genre
FROM events e
JOIN venues v ON e.venue_id = v.id
JOIN performances p ON e.id = p.event_id
JOIN artists a ON p.artist_id = a.id
JOIN performance_genres pg ON p.id = pg.performance_id
JOIN genres g ON pg.genre_id = g.id
WHERE ST_DWithin(v.location, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, 10000)
AND g.name = %s
ORDER BY e.start_date ASC;
"""

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dummy_mp3_path = path.join(path.dirname(__file__), "example-advert.mp3")

# Configure logging
logger.add("logs/event_advert.log", rotation="1 MB", retention="10 days", level="INFO")

# Load API keys
mistral_api_key = "2b4e75c1e1b34aa287a78152394e316e"
lmnt_api_key = "2ycrdMPL6UmtJhlj2pjhmSjt2q5FLrTZ"

# Paths for data storage
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "../data")
os.makedirs(data_dir, exist_ok=True)
output_audio_path = os.path.join(data_dir, "advert.mp3")


class EventData(BaseModel):
    event: dict


# Initialize LLM Model
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

    def __init__(
        self,
        api_key: str,
        model: str = "aurora",
        voice_id: str = "lily",
        bg_music_path: str = None,
    ):
        self.api_key = api_key
        self.voice_id = voice_id
        self.model = model
        self.bg_music_path = bg_music_path
        self.output_file = os.path.join(data_dir, "final_advert.mp3")

    def synthesize(self, text: str) -> str:
        """Convert text to speech and save as an MP3 file."""
        with Speech(self.api_key) as speech:
            synthesis = speech.synthesize(text, self.voice_id, model=self.model)

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
            background = AudioSegment.from_file(self.bg_music_path).set_frame_rate(
                voice.frame_rate
            )

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


def fetch_audio_advert(event_data):
    tts_api_url = ""
    response = requests.post(
        tts_api_url,
        json=json.dumps(event_data),
        headers={"Content-Type": "application/json"},
    )
    return response.content


def generate_event_advert(event_data: dict):
    """Generate an advertisement and add background music."""

    formatted_prompt = prompt.format(
        artist_name=event_data["artist_name"],
        event_type=event_data["event_type"],
        venue_name=event_data["venue_name"],
        city=event_data["city"],
        country=event_data["country"],
        event_start_date=event_data["event_start_date"],
        event_start_time=event_data["event_start_time"],
        genres=", ".join(event_data["genres"]),
        random_number=random_number,
    )

    try:
        response = model.invoke(formatted_prompt)
        advert_text = response.content.strip()
        logger.info(f"Generated Advert Text: {advert_text}")

        # Background music file (replace with your actual music file path)
        bg_music_path = os.path.join(data_dir, "background_music.mp3")

        # Convert text to speech and add background music
        tts = LMNTtts(api_key=lmnt_api_key, bg_music_path=bg_music_path)
        mp3_file_path = tts.synthesize(advert_text)

        return mp3_file_path
    except Exception as e:
        logger.error(f"Error generating advert: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error generating advert: {str(e)}"
        )


@app.get("/")
def hello_world():
    return "Hello, World!"


@app.post("/generated-ads/")
def generated_ads(user_input: UserInput):
    mp3_file_path = None

    try:
        conn_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}?options=endpoint%3D{db_host.split('.')[0]}"
        conn = psycopg.connect(conn_string)
        cur = conn.cursor()
        cur.execute(
            event_by_genre_by_location_query,
            (user_input.lon, user_input.lat, user_input.genre),
        )
        result = cur.fetchall()

        # Call the TTS API to generate an audio file
        # return audio file
        logger.info(
            f"Successfully connected to the database: result count: {len(result)}"
        )

        print(result)

        if len(result) == 0:
            raise HTTPException(
                status_code=404,
                detail="No events found for the given location and genre",
            )

        mp3_file_path = generate_event_advert({"event": result})

        cur.close()
        conn.close()
    except HTTPException as HTTPError:
        if HTTPError.status_code == 404:
            raise HTTPError
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating advert: {str(e)}"
        )

    return FileResponse(mp3_file_path, media_type="audio/mpeg", filename="advert.mp3")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
