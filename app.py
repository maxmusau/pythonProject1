#APIs
# Signup
# Signin
# fetchconference rooms
# Mpesa integration
from flask import *
import pymysql
app=Flask(__name__)
# API-Application programming interface
connection=pymysql.connect(host="localhost",user="root",
                           database="conference__room",password="")
@app.route("/signup",methods=['POST','GET'])
def Signup():
    json=request.json
    username=json['username']
    email = json['email']
    phone = json['phone']
    password = json['password']
    confirm_password = json['confirm_password']
#     validation checks
    if "@" not in email:
        response=jsonify({"message":"Invalid Email"})
        response.status_code=401
        return response
    if password != confirm_password:
        response = jsonify({"message": "Password do not match confirm password"})
        response.status_code = 402
        return response
    sql1="select * from users where username=%s"
    cursor=connection.cursor()
    cursor.execute(sql1,username)
    if cursor.rowcount==1:
        response = jsonify({"message": "Username already exists"})
        response.status_code = 403
        return response
    else:
        #user does not exist
        sql2='insert into users(username,email,phone,password) values(%s,%s,%s,%s)'
        cursor2=connection.cursor()
        cursor2.execute(sql2,(username,email,phone,password))
        connection.commit()
        response = jsonify({"message": "Signup Successful"})
        response.status_code = 200
        return response

@app.route("/signin",methods=['POST','GET'])
def Signin():
    json=request.json
    username=json['username']
    password=json['password']
    sql='select * from users where username=%s and password =%s'
    cursor=connection.cursor()
    cursor.execute(sql,(username,password))
    if cursor.rowcount ==0:
        response = jsonify({"message": "Username does not exist"})
        response.status_code = 405
        return response
    else:
        response = jsonify({"message": "Signin Successful"})
        response.status_code = 201
        return response
@app.route("/save_room",methods=['POST','GET'])
def Save_room():
    json=request.json
    room_name=json['room_name']
    room_desc = json['room_desc']
    cost = json['cost']
    availability = json['availability']
    num_of_people = json['num_of_people']
    image_url = json['image_url']
    sql='insert into conference_rooms(room_name,room_desc,cost,availability,num_of_people,image_url) values(%s,%s,%s,%s,%s,%s)'
    cursor=connection.cursor()
    cursor.execute(sql,(room_name,room_desc,cost,availability,num_of_people,image_url))
    connection.commit()
    response = jsonify({"message": "Conference room saved"})
    response.status_code = 202
    return response
@app.route("/getconferencerooms",methods=['POST','GET'])
def GetConferenceRooms():
    sql='select * from conference_rooms'
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    if cursor.rowcount ==0:
        response = jsonify({"message": "No conference room to display"})
        response.status_code = 406
        return response
    else:
        rooms=cursor.fetchall()
        response=jsonify(rooms)
        response.status_code=203
        return response

        return response




app.run(debug=True)