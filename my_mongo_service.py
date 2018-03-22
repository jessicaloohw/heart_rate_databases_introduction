from flask import Flask, jsonify, request
from main import add_heart_rate, create_user
from pymodm import connect, errors
from datetime import datetime
import models
import numpy as np

app = Flask(__name__)
connect("mongodb://vcm-3486.vm.duke.edu:27017/heart_rate_app")

def validate_input_post(input):

    try:
        user_email = input["user_email"]
        user_age = input["user_age"]
        user_heart_rate = input["heart_rate"]
        assert(type(user_email) == str)
        assert(type(user_age) == int)
        assert((type(user_heart_rate) == int) or (type(user_heart_rate) == float))
        return user_email, user_age, user_heart_rate
    except KeyError:
        return None, None, None
    except AssertionError:
        return None, None, None

def validate_input_interval_average(input):
    try:
        user_email = input["user_email"]
        time_string = input["heart_rate_average_since"]
        assert(type(user_email) == str)
        assert(type(time_string) == str)
        time_formatted = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f")
        return user_email, time_string, time_formatted
    except KeyError:
        return None, None, None
    except AssertionError:
        return None, None, None
    except ValueError:
        return None, None, None

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

@app.route("/api/heart_rate", methods=["POST"])
def api_heart_rate_post():

    input = request.get_json()
    user_email, user_age, user_heart_rate = validate_input_post(input)
    if(user_email is None):
        data = {"message": "Wrong inputs."}
        return jsonify(data), 400

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        add_heart_rate(email=user_email, heart_rate=user_heart_rate, time=datetime.now())
        data = {"message": "Heart rate added to user."}
        return jsonify(data), 200
    except errors.DoesNotExist:
        create_user(email=user_email, age=user_age, heart_rate=user_heart_rate)
        data = {"message": "New user created."}
        return jsonify(data), 200

@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def api_heart_rate_get(user_email):

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        data = {"user_email": user.email,
                "heart_rate": user.heart_rate}
        return jsonify(data), 200
    except errors.DoesNotExist:
        data = {"message": "User not found."}
        return jsonify(data), 400

@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def api_heart_rate_average(user_email):

    try:
        user = models.User.objects.raw({"_id":user_email}).first()
        heart_rate = user.heart_rate
        average_heart_rate = np.mean(heart_rate)
        data = {"user_email": user.email,
                "average_heart_rate": average_heart_rate}
        return jsonify(data), 200
    except errors.DoesNotExist:
        data = {"message": "User not found."}
        return jsonify(data), 400

@app.route("/api/heart_rate/interval_average", methods=["POST"])
def api_heart_rate_interval_average():

    input = request.get_json()
    user_email, time_string, time_formatted = validate_input_interval_average(input)
    if(user_email is None):
        data = {"message": "Wrong inputs."}
        return jsonify(data), 400

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
        return jsonify(data), 200
    except errors.DoesNotExist:
        data = {"message": "User not found."}
        return jsonify(data), 400
