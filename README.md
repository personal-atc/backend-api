# backend-api

docker build -t flask-app .

docker run -p 5000:5000 flask-app

curl -X POST -F "image=@image.jpg http://localhost:5000/upload
