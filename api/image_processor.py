import requests
import base64

# Set up the Secret Manager client
client = secretmanager.SecretManagerServiceClient()

# Specify the secret name and version
secret_name = "projects/69026013544/secrets/openai_key/versions/1"

# Access the secret
response = client.access_secret_version(request={"name": secret_name})
api_key = response.payload.data.decode("UTF-8")

# Set up your API key and endpoint
api_key = "your_api_key"
url = "https://api.openai.com/v1/images/generations"

# Read the image file and convert it to base64
with open("image.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

# Set up the request payload
payload = {
    "prompt": "Question: What is the main subject of this image?",
    "image": image_data
}

# Set up the request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Send the request to the GPT-4 API
response = requests.post(url, json=payload, headers=headers)

# Check the response status code
if response.status_code == 200:
    # Parse the response JSON
    result = response.json()
    
    # Extract the generated answer
    answer = result["choices"][0]["text"]
    print("GPT-4's answer:", answer)
else:
    print("Error:", response.status_code, response.text)