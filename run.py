from api.image_processor import get_secret, get_possible_message, upload_to_gcs
from api.text_to_speech import tts_openai


if __name__ == "__main__":
    api_key = get_secret()
    print("secret done, uploading image")
    bucket_name = "images_from_client"
    url = upload_to_gcs(bucket_name, "image-3.jpg")
    print("image has been uploaded, GPT step")
    messages = []
    message = get_possible_message(url, messages, api_key)
    messages.append(message)
    print("Message: ", message)
    # tts_openai(message, api_key, bucket_name)

    message = get_possible_message(url, messages, api_key)
    messages.append(message)
    print("Message: ", message)
    # tts_openai(message, api_key, bucket_name)
