# pylint: disable=unused-argument
import base64


def lambda_handler(event, context):
    with open("example-advert.mp3", "rb") as f:
        mp3_data = f.read()
    encoded_data = base64.b64encode(mp3_data).decode("utf-8")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "audio/mpeg"},
        "isBase64Encoded": True,
        "body": encoded_data,
    }
