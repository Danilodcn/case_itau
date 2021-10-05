import os
from flask import Flask, jsonify, request
from datetime import datetime
from pymongo import MongoClient
from redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler
from redis.client import Script


HOST = os.getenv("FLASK_HOST", "127.0.0.1")
PORT = os.getenv("FLASK_PORT", 3000)
URL_LOGIN = os.getenv("FLASK_URL_LOGIN", "/api/login")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False")
FLASK_DEBUG = False if FLASK_DEBUG == "False" else True

url = "mongodb://127.0.0.1:27017/"
redis = Redis("localhost", 6379, password="redis_password")
db_mongo = MongoClient(url)
count_mongo = db_mongo["Itau"]["contador"]

valor = count_mongo.find_one({"_id": 0})

if valor == None:
    count = 0
else:
    count = valor["count"]

redis.set("Itau:count:number visitor", count)


app = Flask(__name__)

def conexao_com_mongo():

    number = redis.get("Itau:count:number visitor")

    valor = count_mongo.find_one({"_id": 0})
    if valor == None:
        data = {"_id": 0, "count": 1}
        count_mongo.insert_one(data)
    else:
        data = {"_id": 0, "count": number}
        count_mongo.find_one_and_replace({"_id": 0}, data)

    number_mongo = int(valor["count"])

    # print("Mais um: ", datetime.now())
    print(f"Armazenado no REDIS:\t{int(number)} acessos")
    print(f"Armazenado no MongoDB:\t{number_mongo} acessos \n")

scheduler = BackgroundScheduler()
scheduler.add_job(conexao_com_mongo, "interval", seconds=3)
scheduler.start()


@app.route("/api", methods=["GET"])
def home():
    return "Olá mundo!!!" + str(URL_LOGIN)

@app.route(URL_LOGIN, methods=["POST"])
def login():
    data = request.get_json()
    try: 
        valor = redis.incrby("Itau:count:number visitor")
        output = {"error": "nothing"}
    except:
        output = {"error": "error when incrementing"}
    
    # import ipdb; ipdb.set_trace()
    return jsonify(output)

if __name__ == "__main__":
    try:
        print("Run flask app")
        app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
    except Exception as error:
        print("erro: ", error)
        scheduler.shutdown()