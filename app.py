from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import os
import logging
from api.image_processor import get_secret, get_possible_message, upload_to_gcs
from api.text_to_speech import tts_openai

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' in request.json:
        image_data = request.json['image']
        try:
            decoded_image = base64.b64decode(image_data)
            image = Image.open(BytesIO(decoded_image))
            logging.info('Image decoded and opened successfully.')
            
            temp_image_path = f'temp_image.{image.format.lower()}'
            image.save(temp_image_path)
            logging.info(f'Image saved temporarily as {temp_image_path}.')
            
            api_key = get_secret()
            bucket_name = "images_from_client"
            logging.info('API key and bucket name retrieved.')
           
            url = upload_to_gcs(bucket_name, temp_image_path)
            logging.info(f'Image uploaded to GCS. URL: {url}')
            
            messages = []
            message = get_possible_message(url, messages, api_key)
            logging.info(f'Message extracted: {message}')
            
            if message is None:
                logging.error('No message extracted. Exiting.')
                os.remove(temp_image_path)
                return jsonify({'error': 'No message extracted'}), 400
            
            tts_response = tts_openai(message, api_key, bucket_name)
            logging.info(f'TTS response: {tts_response}')
            
            if tts_response is None:
                logging.error('TTS response is null. Exiting.')
                os.remove(temp_image_path)
                return jsonify({'error': 'TTS response is null'}), 400
            
            os.remove(temp_image_path)
            return jsonify({'tts_response': tts_response})
        except Exception as e:
            logging.error(f'Error in processing: {e}')
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No image provided'}), 400

@app.route('/')
def hello():
    return 'Hello, Dear Flask!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
