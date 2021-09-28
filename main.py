from flask import Flask, jsonify
from json import loads
from Logger import Logger
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
from deta import Deta
from os import environ

app = Flask(__name__)
CORS(app)

deta = Deta(environ.get("DETA_PROJECT_KEY"))


@app.route("/", methods=["GET"])
def home():
    return "Home Page Route"


@app.route("/cached/<branch>", methods=["GET"])
def cached(branch):
    branch = branch.upper()
    db = deta.Base(branch)

    data = db.get("2wuho2fvwmnh")

    if data:
        return jsonify(data)
    else:
        with open(f"./tmp/data/data_{branch}.json", mode="r") as my_file:
            data = loads(my_file.read())
            return jsonify(data)


@app.route("/fetch/<branch>", methods=["GET"])
def latest(branch):
    branch = branch.upper()
    ret = Logger(branch)
    return jsonify(ret.Ret_Links())


@app.route("/refetch", methods=["GET"])
def refetch():
    print("refetching")
    branches = ["ECE", "AIR_A", "AIR_B"]

    for branch in branches:
        Logger(branch).Ret_Links()
        print(f"refetched {branch}")

    return "Refetched"


def scheduledRefetch():
    print("refetching")
    branches = ["ECE", "AIR_A", "AIR_B"]

    for branch in branches:
        Logger(branch).Ret_Links()
        print(f"refetched {branch}")

    return "Refetched"


scheduler = BackgroundScheduler()
job = scheduler.add_job(scheduledRefetch, "interval", minutes=30)
scheduler.start()
