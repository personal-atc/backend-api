import requests
import base64
import os
import uuid

from google.cloud import secretmanager
from google.cloud import storage
from openai import OpenAI


def get_secret():
    # Set up the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Specify the secret name and version
    secret_name = "projects/69026013544/secrets/openai_key/versions/1"

    # Access the secret
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")


def upload_to_gcs(bucket_name, source_file_name):
    """Uploads a file to Google Cloud Storage with a random file name."""
    storage_client = storage.Client(project="personal-atc")
    bucket = storage_client.bucket(bucket_name)
    
    # Generate a random file name
    extension = os.path.splitext(source_file_name)[1]
    random_file_name = f"{uuid.uuid4()}{extension}"
    
    blob = bucket.blob(random_file_name)

    blob.upload_from_filename(source_file_name)

    # Make the blob publicly viewable
    blob.make_public()

    return blob.public_url


def ask_question_about_image(url, question, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": question},
            {
            "type": "image_url",
            "image_url": {
                "url": url,
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    return response.choices[0]

# Example usage
# image_response = upload_image('path/to/your/image.jpg')
# if image_response:
#     question_response = ask_question_about_image(image_response['image_id'], "What is in this image?")
#     print(question_response)
