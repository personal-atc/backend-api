from api.image_processor import get_secret, ask_question_about_image, upload_to_gcs


if __name__ == "__main__":
    api_key = get_secret()
    print("secret done, uploading image")
    url = upload_to_gcs("images_from_client", "image.jpg")
    print("image has been uploaded, GPT step")
    print(ask_question_about_image(url, "what do you see here?", api_key))