from flask import Flask, request, jsonify
from PIL import Image
from api.image_processor import get_secret, get_possible_message, upload_to_gcs
from api.text_to_speech import tts_openai
import os

app = Flask(__name__)
messages_history = []

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image_file = request.files['image']
        try:            
            image = Image.open(image_file)            
            temp_image_path = f'temp_image.{image.format.lower()}'
            image.save(temp_image_path)            
            api_key = get_secret()
            bucket_name = "images_from_client"            
            url = upload_to_gcs(bucket_name, temp_image_path)
            global messages_history
            message = get_possible_message(url, messages_history, api_key)
            messages_history.append(message)            
            if message == "NOTHING":
                os.remove(temp_image_path)
                return jsonify({'tts_response': ''})            
            tts_response = tts_openai(message, api_key, bucket_name)            
            os.remove(temp_image_path)            
            return jsonify({'tts_response': tts_response})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No image provided'}), 400

@app.route('/')
def hello():
    return 'Hello, Dear Flask!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')