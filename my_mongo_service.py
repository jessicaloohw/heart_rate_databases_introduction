from flask import Flask, jsonify, request
from main import add_heart_rate, create_user
from pymodm import connect
from datetime import datetime
import models

app = Flask(__name__)

@app.route("/api/heart_rate", methods=["POST"])
def api_heart_rate_post():

    connect("mongodb://vcm-3486.vm.duke.edu:27017/heart_rate_app")

    input = request.get_json()
    user_email = input["user_email"]
    user_age = input["user_age"]
    user_heart_rate = input["heart_rate"]

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        add_heart_rate(email=user_email, heart_rate=user_heart_rate, time=datetime.now())
        data = {"message": "Heart rate added to user."}
        return jsonify(data)
    except:
        create_user(email=user_email, age=user_age, heart_rate=user_heart_rate)
        data = {"message": "New user created."}
        return jsonify(data)

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def api_heart_rate_get(user_email):

    connect("mongodb://vcm-3486.vm.duke.edu:27017/heart_rate_app")

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        data = {"user_email": user.email,
                "heart_rate": user.heart_rate}
        return jsonify(data)
    except:
        data = {"message": "User not found."}
        return jsonify(data)

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def api_heart_rate_average(user_email):

    import numpy as np

    connect("mongodb://vcm-3486.vm.duke.edu:27017/heart_rate_app")

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        heart_rate = user.heart_rate
        average_heart_rate = np.mean(heart_rate)
        data = {"user_email": user.email,
                "average_heart_rate": average_heart_rate}
        return jsonify(data)
    except:
        data = {"message": "User not found."}
        return jsonify(data)

def check_tachycardia(user_age, user_average_heart_rate):

    if(user_age < 3):
        if(user_average_heart_rate > 151):
            return True
        else:
            return False
    elif(user_age > 2 and user_age < 5):
        if(user_average_heart_rate > 137):
            return True
        else:
            return False
    elif(user_age > 4 and user_age < 8):
        if(user_average_heart_rate > 133):
            return True
        else:
            return False
    elif(user_age > 7 and user_age < 12):
        if(user_average_heart_rate > 130):
            return True
        else:
            return False
    elif(user_age > 11 and user_age < 16):
        if(user_average_heart_rate > 119):
            return True
        else:
            return False
    else:
        if(user_average_heart_rate > 100):
            return True
        else:
            return False

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def api_heart_rate_interval_average():

    import numpy as np

    connect("mongodb://vcm-3486.vm.duke.edu:27017/heart_rate_app")

    input = request.get_json()
    user_email = input["user_email"]
    time_string = input["heart_rate_average_since"]
    time_formatted = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f")

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        age = user.age
        heart_rate = user.heart_rate
        heart_times = user.heart_rate_times

        valid_heart_rates = []
        for n,t in enumerate(heart_times):
            if(t > time_formatted):
                valid_heart_rates.append(heart_rate[n])
        interval_average = np.mean(valid_heart_rates)

        tachycardia = str(check_tachycardia(age, interval_average))

        data = {"user_email": user.email,
                "heart_rate_average_since": time_string,
                "interval_average": interval_average,
                "tachycardia": tachycardia}
        return jsonify(data)
    except:
        data = {"message": "User not found."}
        return jsonify(data)
