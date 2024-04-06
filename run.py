from api.image_processor import get_secret, ask_question_about_image


if __name__ == "__main__":
    api_key = get_secret()
    print(ask_question_about_image("image.jpg", "", api_key))