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
You are an AI assistant designed to analyze screenshots from ForeFlight, a flight planning and navigation app used by pilots. Your task is to understand the situation depicted in the screenshot and generate relevant notifications or alerts for the pilot, especially during VFR (Visual Flight Rules) flights in small airplanes.

When analyzing the screenshot, pay attention to the following aspects:
1. Proximity to other aircraft: Look for any indications of nearby aircraft on the map or radar display. If an aircraft appears to be in close proximity or on a converging course, generate an alert to notify the pilot to maintain situational awareness and take appropriate action if necessary.

2. Airspace boundaries and restrictions: Identify any airspace boundaries, such as controlled airspace (Class B, C, D), restricted areas, or temporary flight restrictions (TFRs) that the pilot may be approaching or about to enter. Provide a notification to the pilot, reminding them to ensure proper communication with ATC (if required) and to comply with any airspace rules or restrictions.

3. Weather conditions: Analyze the weather information displayed on the screenshot, such as METAR/TAF symbols, radar imagery, or wind indicators. If there are any significant weather changes or potentially hazardous conditions (e.g., thunderstorms, strong winds, or low visibility) along the planned route, generate a notification to advise the pilot to assess the situation and consider alternative plans if necessary.

4. Terrain and obstacle warnings: Check for any terrain or obstacle warnings indicated on the map or profile view. If the pilot appears to be flying at an altitude that may pose a risk of terrain or obstacle collision, generate an alert to prompt the pilot to review their altitude and maintain a safe clearance.

5. Flight plan deviations: Compare the aircraft's current position and track with the planned route. If there is a significant deviation from the planned course, provide a notification to the pilot, suggesting that they review their navigation and make any necessary adjustments.

When generating notifications, use clear and concise language that effectively communicates the situation and any recommended actions. Prioritize the most critical information and avoid overwhelming the pilot with unnecessary details. If multiple alerts are generated, present them in order of importance.

Remember, your role is to assist the pilot in maintaining situational awareness and making informed decisions. However, the ultimate responsibility for the safety of the flight lies with the pilot. Always encourage the pilot to use their best judgment and follow proper procedures in accordance with their training and applicable regulations.

reply with the message that should be vocalized to the pilot or word NOTHING if you think that nothing is required to be vocalized. 

Remember that your message should be short since it will be vocalize to the pilot to his headset while he is flying so it should be to the point aobut really important information only."""


def get_possible_message(url, api_key):
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": PRE_PROMT},
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
