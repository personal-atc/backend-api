from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from api.image_processor import get_secret, get_possible_message, upload_to_gcs
from api.text_to_speech import tts_openai
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.json:
        image_data = request.json['image']
        try:
            decoded_image = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_image))
            
            temp_image_path = f'temp_image.{image.format.lower()}'
            
            image.save(temp_image_path)
            
            api_key = get_secret()
            bucket_name = "images_from_client"
           
            url = upload_to_gcs(bucket_name, temp_image_path)
            
            messages = []
            message = get_possible_message(url, messages, api_key)
            
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
