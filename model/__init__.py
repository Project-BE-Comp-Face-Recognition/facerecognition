from app import app
from flask import request, session
from helpers.database import *
from helpers.hashpass import *
from helpers.mailer import *
from helpers.recognition import *
from bson import json_util, ObjectId
import json


def checkloginusername():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    if check is None:
        return "No User"
    else:
        return "User exists"


def checkloginpassword():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    password = request.form["password"]
    hashpassword = getHashed(password)
    if hashpassword == check["password"]:
        session["username"] = username
        return "correct"
    else:
        return "wrong"


def checkusername():
    username = request.form["username"]
    check = db.users.find_one({"username": username})
    if check is None:
        return "Available"
    else:
        return "Username taken"


def checkemail():
    email = request.form["email"]
    check = db.users.find_one({"email": email})
    if check is None:
        return "Available"
    else:
        return "Email taken"


def checkFaceGroupName():
    groupname = request.form["groupname"]
    check = db.facegroup.find_one({"groupname": groupname})
    if check is None:
        return "Available"
    else:
        return "Class with Same Name Already Present"


def registerUser():
    fields = [k for k in request.form]
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = getHashed(user_data["password"])
    user_data["confirmpassword"] = getHashed(user_data["confirmpassword"])
    db.users.insert(user_data)
    sendmail(subject="Registration for Flask Admin Boilerplate", sender="Flask Admin Boilerplate",
             recipient=user_data["email"], body="You successfully registered on Flask Admin Boilerplate")


def fetchAttendance():

    res = db.attendance.find()
    return res


def fetchstudent():

    res = db.users.find()

    return res


def fetchSubjectAttendance():

    res = db.attendance.find({}, {"sub1": 1, "_id": 0})
    li = []
    for i in res:
        a = int(i["sub1"])
        li.append(a)
    return li


def fetchlabelAttendance():

    res = db.attendance.find({}, {"branch": 1, "_id": 0})
    li = []
    for i in res:
        a = i["branch"]
        li.append(a)
    return li


'''
Face Recognition Start
'''


def createPersonGroup(PERSON_GROUP_ID):
    print('Person group:', PERSON_GROUP_ID)
    try:
        face_client.person_group.create(
            person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
    except:
        print("error while creating class")


def addGroupName():
    fields = [k for k in request.form]
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    db.facegroup.insert(user_data)
    classname = values[0]
    return classname


def fetchTimetable():

    res = db.timetable.find({}, {"be-comp": 1, "_id": 0})
    li = []
    for i in res:
        a = i["be-comp"]
        li.append(a)
    
    return li


'''
Face Recogniton End
'''
