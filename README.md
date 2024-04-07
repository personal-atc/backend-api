# backend-api

docker build -t flask-app .

docker run -p 5000:5000 flask-app

curl -X POST http://localhost:5000/upload -H "Content-Type: application/json" -d @t.txt

t.txt -> {"image":"<base64>"}
