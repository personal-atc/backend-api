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

PRE_PROMT = """
You are an AI assistant designed to analyze static screenshots from ForeFlight. Your task is to understand the situation depicted in the screenshot to the best of your ability and generate relevant notifications or alerts for the pilot. Assume that pilot is doing VFR flight in a small airplanes.
When analyzing the screenshot, pay attention to the following aspects:
* Proximity to other aircraft: Look for any indications of nearby aircraft on the map or radar display. If an aircraft appears to be in close proximity or on a converging course, generate a concise alert to notify the pilot.
* Airspace boundaries and restrictions: Identify any airspace boundaries, such as controlled airspace (Class B, C, D), restricted areas, or temporary flight restrictions (TFRs) that the pilot may be approaching or about to enter. Provide a brief notification to the pilot.
* Weather conditions: Analyze the weather information displayed on the screenshot, such as METAR/TAF symbols, radar imagery, or wind indicators. If there are any significant weather changes or potentially hazardous conditions (e.g., thunderstorms, strong winds, or low visibility) along the planned route, generate a short notification to advise the pilot.
* Terrain and obstacle warnings: Check for any terrain or obstacle warnings indicated on the map or profile view. If the pilot appears to be flying at an altitude that may pose a risk of terrain or obstacle collision based on the information in the screenshot, generate a concise alert.
* Flight plan deviations: Compare the aircraft's current position and track with the planned route. If there is a significant deviation from the planned course, provide a brief notification to the pilot.

When generating notifications, use clear and concise language that effectively communicates the critical information to the pilot based on the static screenshot. Prioritize the most essential details and keep the messages brief, as they will be vocalized to the pilot's headset while flying.
Reply with the message that should be vocalized to the pilot or the word "NOTHING" if you think that no vocalization is required based on the current screenshot or on the history of messages.
Keep in mind that you will be receiving screenshots every 5 seconds, so check the message history to avoid repeating the same notification unnecessarily.

Message history:
"""


def get_possible_message(url, history_of_messages, api_key):
    prompt = ""
    if history_of_messages:
        prompt = PRE_PROMT + "\nmessage: ".join(history_of_messages)
    else:
        prompt = PRE_PROMT + "\n no prev messages"

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
            "type": "image_url",
            "image_url": {
                "url": url,
            },
            },
        ],
        }
    ],
    max_tokens=600,
    )

    msg = response.choices[0].message.content
    if msg == "I'm sorry, but I can't provide assistance with that request.":
        return "NOTHING"
    if "I'm sorry" in msg:
        return "NOTHING"
    return msg

# Example usage
# image_response = upload_image('path/to/your/image.jpg')
# if image_response:
#     question_response = ask_question_about_image(image_response['image_id'], "What is in this image?")
#     print(question_response)
