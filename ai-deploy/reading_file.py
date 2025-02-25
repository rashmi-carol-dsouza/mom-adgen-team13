import json
import os
import boto3

# Initialize S3 client
s3 = boto3.client("s3")

# Define your S3 bucket name
BUCKET_NAME = "event-advert-mp3-storage"
FILE_NAME = "background.mp3"

def lambda_handler(event, context):
    try:
        # Check if the file exists in S3
        response = s3.head_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"File {FILE_NAME} exists in S3.",
                "size": response["ContentLength"],
                "last_modified": response["LastModified"].isoformat(),
                "etag": response["ETag"]
            })
        }

    except s3.exceptions.ClientError as e:
        # If the file is not found
        if e.response['Error']['Code'] == '404':
            return {
                "statusCode": 404,
                "body": json.dumps({"message": f"File {FILE_NAME} not found in S3."})
            }
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"message": "Error accessing S3.", "error": str(e)})
            }
