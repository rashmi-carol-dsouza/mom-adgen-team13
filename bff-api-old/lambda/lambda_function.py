# pylint: disable=unused-argument
import base64
import json

import requests
from query import event_by_genre_by_location_query


def fetch_audio_advert(event_data):
    tts_api_url = ""
    response = requests.post(
        tts_api_url,
        json=json.dumps(event_data),
        headers={"Content-Type": "application/json"},
    )
    return response.content


def lambda_handler(event, context):
    body = json.loads(event.get("body", "{}"))

    latitude = body.get("lat")
    longitude = body.get("lon")
    genre = body.get("genre")[0]
    language = body.get("language")

    db_name = "koyebdb"
    db_user = "koyeb-adm"
    db_password = "npg_4ABuiR8rKdwW"
    db_host = "ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app"

    # try:
    #     conn_string = f"postgresql://{db_user}:{db_password}@{db_host}/{db_name}?options=endpoint%3D{db_host.split('.')[0]}"
    #     conn = psycopg2.connect(conn_string)
    #     cur = conn.cursor()
    #     cur.execute(event_by_genre_by_location_query, (longitude, latitude, genre))
    #     result = cur.fetchall()

    #     # Call the TTS API to generate an audio file
    #     # return audio file

    #     cur.close()
    #     conn.close()
    # except Exception as e:
    #     print("Error connecting to the database:", e)

    with open("example-advert.mp3", "rb") as f:
        mp3_data = f.read()
        encoded_data = base64.b64encode(mp3_data).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "audio/mpeg",
            "Access-Control-Allow-Origin": "*",  # Allows all domains
            "Access-Control-Allow-Methods": "OPTIONS, POST, GET",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "isBase64Encoded": True,
        "body": encoded_data,
    }
