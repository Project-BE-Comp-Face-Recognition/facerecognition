from app import app
from flask import request, session
from helpers.database import *
from helpers.hashpass import *
from helpers.mailer import *
from helpers.recognition import *
from helpers.path import *
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
    sendmail(subject="Registration for Flask Admin Boilerplate", sender="Flask Admin Boilerplate", recipient=user_data["email"], body="You successfully registered on Flask Admin Boilerplate")
    studentData={k:v for k,v in data.items() if (k=="username" or k=="name" or k=="email" or k=="mobile" or k=="rollnumber")}
    try :
        db.users.insert(user_data)
        db.studentdataset.insert(studentData)
        print("Succesully added Registration Data to DB")
    except:
        print("Failed to Add Registration Data In DB")
        return False
    return True



def fetchAttendance():
    res = db.attendance.find()    
    return res


#display timetable
def fetchTimetable():
    
    res = db.timetable.find({},{"class":1,"_id":0})
    li=[] 
    for i in res:
        a=i["class"]["be-comp"]
        li.append(a) 
    return li
    
     
#admin register   
def fetchstudent():
    res = db.users.find()
    return res
   
#attendance table
def fetchSubjectAttendance():
    res = db.attendance.find({}, {"sub1": 1, "_id": 0})
    li = []
    for i in res:
        a=int(i["sub1"])
        li.append(a)
    return li

#Subject 
def fetchlabelAttendance():
    res = db.attendance.find({}, {"branch": 1, "_id": 0})
    li = []
    for i in res:
        a=i["branch"]
        li.append(a)
    return li
    
'''
Face Recognition Start
'''
def createPersonGroup(PERSON_GROUP_ID):
    print('Person group:', PERSON_GROUP_ID)
    try:
        face_client.person_group.create(person_group_id=PERSON_GROUP_ID, name=PERSON_GROUP_ID)
    except :
        print("error while creating class")

def addGroupName():
    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    db.facegroup.insert(user_data)
    classname=values[0]
    return classname

def personGroupPerson(classroom,prn):
    userID = face_client.person_group_person.create(classroom,prn)
    print("PersonId--->",userID.person_id)
    
    return userID.person_id

def addPersonIdToDb(personId,prn):
    try :
        db.studentdataset.update_one({"username":prn},{"$set":{"personId":personId}},upsert=False)
        print("Succesfully Added Person Id to DB")
    except:
        print("Error while Adding Unique Id to DB")
        return False
    return True

def fetchTimetable():
    res = db.timetable.find({}, {"class": 1, "_id": 0})
    li = []
    for i in res:
        a = i["class"]
        li.append(a)
    
    return li


'''
Face Recogniton End
'''
def studentregistration():

    h=str(home)+'\static'
    target = os.path.join(h, "train/")
    if not os.path.isdir(target):
        os.mkdir(target)
    classname = str(request.form['classroom'])
    session['classfolder'] = classname
    classpath = os.path.join(target, str(request.form["classroom"])+"/")
    session['classpath'] = classpath
    if not os.path.isdir(classpath):
        os.mkdir(classpath)

    prn = str(request.form["username"])
    session['studetnfolder'] = prn
    studentfolderpath = os.path.join(classpath, prn+"/")
    if not os.path.isdir(studentfolderpath):
        os.mkdir(studentfolderpath)

    for file in request.files.getlist("files[]"):
        filename = file.filename
        destination = "/".join([studentfolderpath, filename])
        file.save(destination)
    
    registrationStatus=registerUser()
    if registrationStatus== True:
        uniquePersonId=personGroupPerson(classname,prn)
        status=addPersonIdToDb(uniquePersonId,prn)
        if status == True:
            print("Generated Unique ID and Upadted in DB")
            return "Successful"
    return "Failed"


def showClassroom():
    classroom=[]
    result=db.facegroup.find({},{"groupname":1,"_id":0})
    for val in result:
        classroom.append(val["groupname"])
    return classroom
  
  #delete button
def delet(email_del):
    db.users.remove({"email" : email_del})
  
#Edit button
def fetchuser(email_find):
    users = db.users.find_one({"email":email_find})
    return users
    
def updateuser(email):
    name = request.form['name']
    clas = request.form['class']
    rno = request.form['roll number']
    db.users.update({"email": email},
                   {"$set": {
                      "name" : name,
                      "class" : clas,
                      "roll_number" : rno}})
  
# Edit Profile
def findprofile(uname):
    users = db.users.find_one({"username":uname})
    return users
    
def saveprofile(uname):
    name = request.form['name']
    clas = request.form['class']
    rno = request.form['roll number']
    age = request.form['age']
    number = request.form['number']
    db.users.update_one({"username": uname},
                   {"$set": {
                      "name" : name,
                      "class" : clas,
                      "roll_number" : rno,
                      "age" : age,
                      "number" : number}})     
    
#reset password
def updatepass(uname):
    password = getHashed(request.form['enter_password'])
    confirmpassword = getHashed(request.form['confirm_password'])
    db.users.update_one({"username": uname},
                   {"$set": {
                      "password" : password,
                      "confirmpassword" : confirmpassword}})
    



