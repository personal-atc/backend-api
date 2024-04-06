from openai import OpenAI
from time import time

from api.image_processor import upload_to_gcs


def tts_openai(message, api_key, bucket_name):
    if message == "NOTHING":
        return

    print(message)
    client = OpenAI(api_key=api_key)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=message,
    )

    milliseconds = int(time() * 1000)
    file_name = f"{milliseconds}.mp3"
    response.stream_to_file(file_name)

    upload_to_gcs(bucket_name, file_name)
