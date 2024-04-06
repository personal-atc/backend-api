from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the request has 'image' as base64 string
    if 'image' in request.json:
        image_data = request.json['image']
        # Decode the base64 string
        try:
            decoded_image = base64.b64decode(image_data)
            # Convert binary data to an image
            image = Image.open(BytesIO(decoded_image))
            # Process the image or save it as needed
            # For demonstration, just show the image format
            image_format = image.format

            return jsonify({'message': 'Image received successfully', 'format': image_format})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No image provided'}), 400

@app.route('/')
def hello():
    return 'Hello, Dear Flask!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
