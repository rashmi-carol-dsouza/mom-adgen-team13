# pylint: disable=unused-argument
import base64

import psycopg2


def lambda_handler(event, context):
    db_name = "koyebdb"
    db_user = "koyeb-adm"
    db_password = "npg_4ABuiR8rKdwW"
    db_host = "ep-aged-forest-a2sd5mrk.eu-central-1.pg.koyeb.app"

    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("Database connection test result:", result)
        cur.close()
        conn.close()
    except Exception as e:
        print("Error connecting to the database:", e)

    with open("example-advert.mp3", "rb") as f:
        mp3_data = f.read()
        encoded_data = base64.b64encode(mp3_data).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "audio/mpeg"},
        "isBase64Encoded": True,
        "body": encoded_data,
    }
