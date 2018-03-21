import requests

# (1) Launch MongoDB on virtual machine
# sudo docker run -v $PWD/db:/data/db -p 27017:27017 mongo
# (2) Launch Flask app on local machine
# FLASK_APP=my_mongo_service.py flask run

# USER 1:
user_data1 = {"user_email": "jessica@gmail.com",
             "user_age": 25,
             "heart_rate": 70}
r1 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=user_data1)
print(r1.json())

user_data2 = {"user_email": "jessica@gmail.com",
             "user_age": 25,
             "heart_rate": 75}
r2 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=user_data2)
print(r2.json())

r3 = requests.get("http://127.0.0.1:5000/api/heart_rate/jessica@gmail.com")
print(r3.json())

r4 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/jessica@gmail.com")
print(r4.json())

time_stamp1 = {"user_email": "jessica@gmail.com",
               "heart_rate_average_since": "2018-03-01 00:00:00.000000"}
r5 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average", json=time_stamp1)
print(r5.json())

# USER 2: Does not exist
r6 = requests.get("http://127.0.0.1:5000/api/heart_rate/nouser@gmail.com")
print(r6.json())

r7 = requests.get("http://127.0.0.1:5000/api/heart_rate/average/nouser@gmail.com")
print(r7.json())

time_stamp2 = {"user_email": "nouser@gmail.com",
               "heart_rate_average_since": "2018-03-01 00:00:00.000000"}
r8 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average", json=time_stamp2)
print(r8.json())

# USER 3: Wrong inputs
user_data3 = {"email": "wronginput@gmail.com",
              "age": 50,
              "heart_rate": 1000}
r9 = requests.post("http://127.0.0.1:5000/api/heart_rate", json=user_data3)
print(r9.json())

time_stamp3 = {"user_email": "wronginput@gmail.com",
               "heart_rate_average_since": "18-01-01 00:00:00.000000"}
r10 = requests.post("http://127.0.0.1:5000/api/heart_rate/interval_average", json=time_stamp3)
print(r10.json())
