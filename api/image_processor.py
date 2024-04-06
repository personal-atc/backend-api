import requests
import base64
from google.cloud import secretmanager
from openai import OpenAI


def get_secret():
    # Set up the Secret Manager client
    client = secretmanager.SecretManagerServiceClient()

    # Specify the secret name and version
    secret_name = "projects/69026013544/secrets/openai_key/versions/1"

    # Access the secret
    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")


API_URL = 'https://api.openai.com/v1/images'


def ask_question_about_image(image_id, question, api_key):
    url = "https://storage.googleapis.com/images_from_client/image.jpg"
    client = OpenAI(key=api_key)

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": "What’s in this image?"},
            {
            "type": "image_url",
            "image_url": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
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
