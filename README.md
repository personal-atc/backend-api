# backend-api

docker build -t flask-app .

docker run -p 5000:5000 flask-app

curl -X POST http://localhost:5000/upload -H "Content-Type: multipart/form-data" -d @image.jpg