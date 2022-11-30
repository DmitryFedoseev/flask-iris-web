sudo docker-compose up --build

sudo docker exec -it flask-ler_flask_1 bash

sudo docker exec -it flask-ler_flask_1 python train_model.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,7"}' \
  http://localhost:5000/iris_post