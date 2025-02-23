import base64
import json
from os import path

import psycopg
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from loguru import logger
from query import event_by_genre_by_location_query

db_name = "koyebdb"
db_user = "koyeb-adm"
db_password = "npg_4ABuiR8rKdwW"
db_host = "ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app"

app = Flask(__name__)

dummy_mp3_path = path.join(path.dirname(__file__), "example-advert.mp3")


def fetch_audio_advert(event_data):
    tts_api_url = ""
    response = requests.post(
        tts_api_url,
        json=json.dumps(event_data),
        headers={"Content-Type": "application/json"},
    )
    return response.content


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/generated-ads", methods=["POST"])
def generated_ads():
    body = request.get_json()
    latitude = body.get("lat")
    longitude = body.get("lon")
    genre = body.get("genre")[0]
    language = body.get("language")

    try:
        conn_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}?options=endpoint%3D{db_host.split('.')[0]}"
        conn = psycopg.connect(conn_string)
        cur = conn.cursor()
        cur.execute(event_by_genre_by_location_query, (longitude, latitude, genre))
        result = cur.fetchall()

        # Call the TTS API to generate an audio file
        # return audio file
        logger.info(
            f"Successfully connected to the database: result count: {len(result)}"
        )

        cur.close()
        conn.close()
    except Exception as e:
        print("Error connecting to the database:", e)
        return jsonify({"error": "Database connection error"}), 500

    with open(dummy_mp3_path, "rb") as f:
        mp3_data = f.read()
        encoded_data = base64.b64encode(mp3_data).decode("utf-8")

    response = jsonify({"audio_data": encoded_data})
    response.headers["Content-Type"] = "application/json"
    response.headers["Content-Disposition"] = "attachment; filename=advert.mp3"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
