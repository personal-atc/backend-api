from api.image_processor import get_secret, get_possible_message, upload_to_gcs


if __name__ == "__main__":
    api_key = get_secret()
    print("secret done, uploading image")
    url = upload_to_gcs("images_from_client", "image-2.jpg")
    print("image has been uploaded, GPT step")
    messages = []
    message = get_possible_message(url, messages, api_key)
    messages.append(message)
    print("Message: ", message)
    message = get_possible_message(url, messages, api_key)
    messages.append(message)
    print("Message: ", message)
