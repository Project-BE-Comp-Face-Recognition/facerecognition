from flask.json import jsonify
from app import app
from flask import request, session
from helpers.database import *
from helpers.hashpass import *
from helpers.mailer import *
from helpers.recognition import *
from helpers.path import *
from bson import json_util, ObjectId
import json,shutil
from datetime import date

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



def registerTeacher():
    fields = [k for k in request.form if k!='subject[]']                                      
    values = [request.form[k] for k in request.form if k!='subject[]']
    data = dict(zip(fields, values))
    subject= request.form.getlist('subject[]')
    data['subject']=subject
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = getHashed(user_data["password"])
    user_data["confirmpassword"] = getHashed(user_data["confirmpassword"])
    subject= request.form.getlist('subject[]')
    try :
        db.teachersdataset.insert(user_data)
        print("Succesully added Registration Data to DB")
    except:
        print("Failed to Add Registration Data In DB")
        return False
    return True


def registerRegisterUser():
    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form] 
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    user_data["password"] = getHashed(user_data["password"])
    user_data["confirmpassword"] = getHashed(user_data["confirmpassword"])
    sendmail(subject="Registration for Flask Admin Boilerplate", sender="Flask Admin Boilerplate", recipient=user_data["email"], body="You successfully registered on Flask Admin Boilerplate")
    try :
        db.users.insert(user_data)
        print("Succesully added Registration Data to DB")
    except:
        print("Failed to Add Registration Data In DB")
        return False
    return True


def registerStudent():
    fields = [k for k in request.form]                                      
    values = [request.form[k] for k in request.form]
    data = dict(zip(fields, values))
    user_data = json.loads(json_util.dumps(data))
    fields =[k for k in request.form if k=="name" or k=="username" or k=="classroom" or k=="rollnumber" or k=="personId" ]                                      
    fields.append("attendance")
    values = [request.form[k] for k in request.form if k=="name" or k=="username" or k=="classroom" or k=="rollnumber" or k=="personId"]
    values.append([])
    attendanceData= dict(zip(fields, values))
    try :
        db.studentdataset.insert(user_data)
        db.attendancelog.insert(attendanceData)
        print("Succesully added Registration Data to DB")
    except:
        print("Failed to Add Registration Data In DB")
        return False
    return True


def fetchAttendance():
    res = db.attendance.find()    
    return res
    
#fetch total attendance
def fetchTotalAttendance():
    res = db.attendance.find({}, {"name": 1, "_id": 0})
    count=0
    for i in res:
        count=count+1
    return count


# Fetch Student Information
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

# Fetch Label for chart creation
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

def addFaceToPersonGroup(PERSON_GROUP_ID,uniquePerosnId,user,studenFolderPath):
    userImageFolder=[filename for filename in os.listdir(studenFolderPath) ]
    print(userImageFolder)
    try :
        for image in userImageFolder:
            print(studenFolderPath+'/'+image)
            i = open(studenFolderPath+'/'+image, 'r+b')
            face_client.person_group_person.add_face_from_stream(PERSON_GROUP_ID, uniquePerosnId, i)
            print("Person added Succesfully")
            print('Pausing for 6 seconds to avoid triggering rate limit on free account...')
        return True
    except:
        print("Error While adding Photo to Classroom")
        return False





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
    try:

        userID = face_client.person_group_person.create(classroom,prn)
        print("PersonId--->",userID.person_id)
        return userID.person_id

    except Exception as e:
        print(e)
        return "error"


def addPersonIdToDb(personId,prn):
    try :
        db.studentdataset.update_one({"username":prn},{"$set":{"personId":personId}},upsert=False)
        db.attendancelog.update_one({"username":prn},{"$set":{"personId":personId}},upsert=False)
        print("Succesfully Added Person Id to DB")
    except:
        print("Error while Adding Unique Id to DB")
        return False
    return True

def fetchTimetable(clasroom):
    res = db.timetable.find({}, {"class": 1, "_id": 0})
    li = []
    for i in res:
        a = i["class"][clasroom]
        li.append(a)
    return li



'''
Face Recogniton End
'''
def studentregistration():

    h=str(home)
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
    
    uniquePersonId=personGroupPerson(classname,prn)
    if uniquePersonId == "error":
        return "error"
    print("Genrated Unique ID")
    addFaceStatus=addFaceToPersonGroup(classname,uniquePersonId,prn,studentfolderpath)
        
    
    if addFaceStatus== True:
        removeTrainDataset(studentfolderpath)
        face_client.person_group.train(classname)    
        while (True):
            training_status = face_client.person_group.get_training_status(classname)
            print("Training status: {}.".format(training_status.status))
            print()
            if (training_status.status is TrainingStatusType.succeeded):
                registrationStatus=registerStudent()
                status=addPersonIdToDb(uniquePersonId,prn)
                if status==True:
                    print("Trained Faces & Generated Unique ID and Upadted in DB")
                    return ("success")
                
            elif (training_status.status is TrainingStatusType.failed):
                face_client.person_group_person.delete(person_group_id=classname,person_id=uniquePersonId,custom_headers=None,raw=False)
                return ("error")        
    else:
        removeTrainDataset(studentfolderpath)
        return ("error")
    
            

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
    
#update password
def updatepass(uname):
    password = getHashed(request.form['enter_password'])
    confirmpassword = getHashed(request.form['confirm_password'])
    db.users.update_one({"username": uname},
                   {"$set": {
                      "password" : password,
                      "confirmpassword" : confirmpassword}})

def checkmail():
    email = request.form["email"]
    check = db.users.find_one({"email": email})
    if check is None:
        return check
    else:
        session["rp_email"] = check['email']
        return check['email']

      
#reset password
def resetpass():
    password = getHashed(request.form['enter_password'])
    confirmpassword = getHashed(request.form['confirm_password'])
    mail = session["rp_email"]
    db.users.update_one({"email": mail},
                   {"$set": {
                      "password" : password,
                      "confirmpassword" : confirmpassword}})

def fetchlabelNameAttendance():
    res = db.attendance.find({}, {"name": 1, "_id": 0})
    li = []
    for i in res:
        a=i["name"]
        li.append(a)
    return li


def removeTrainDataset(path: str )-> None :
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.remove(path)

def checkclass():
    cls = request.form["class"]
    check = db.studentdataset.find({"classroom": cls})
    if check is None:
        return check
    else:
        li=[]
        for i in check:
            li.append(i["email"])
        return li


def markAttendance(identifiedFace,subjectname):
    today = date.today()

    dateToday= today.strftime("%d/%m/%Y")
    for i in identifiedFace:
        res=db.attendancelog.update_one({'personId':i, "attendance.date":dateToday} , {"$inc":{"attendance.$.todaysattendance."+subjectname:1}})
        modified=res.modified_count
        if modified==0:
            ta={subjectname:1}
            k=["date","todaysattendance"]
            v=[dateToday,ta]
            attendance=dict(zip(k,v))
            print(attendance)
            db.attendancelog.update_one({'personId':i},{'$push':{"attendance":attendance}})
            return "success"

        else:
            return "success"




def identifyFace():

    classroom=request.form['classroom']
    teahersId=request.form['teachersId']
    subject=request.form['subject']

    h=str(home)
    target = os.path.join(h, "identify")
    if not os.path.isdir(target):
        os.mkdir(target)
    teacherfolder = os.path.join(target, teahersId+"/")
    if not os.path.isdir(teacherfolder):
        os.mkdir(teacherfolder)
    for file in request.files.getlist("files[]"):
        filename = file.filename
        destination = "/".join([teacherfolder, filename])
        file.save(destination)

    imageName=[filename for filename in os.listdir(teacherfolder) ]
    print(imageName)
    face_ids = []
    identifiedFace=[]

    for image in imageName:
        i = open(teacherfolder+'/'+image, 'r+b')
        try:
            print("Fetching Face Ids ../")
            faces = face_client.face.detect_with_stream(i, detection_model='detection_03')
            face_ids.append(faces[0].face_id)
        except:
            i.close()
            print("No Face Detected")
            removeTrainDataset(target)
            return "error"
    
    i.close()
    removeTrainDataset(target)        
    print("Identified face Ids From Upload-->",face_ids)
    try:
        results = face_client.face.identify(face_ids, classroom)
        if not results:
            print('No person identified in the person group for faces from {}.'.format(imageName))
            return 0
        print("Finding Person ID")
        for person in results:
            if len(person.candidates) > 0:
                print(person.face_id )
                identifiedUniqueId=person.candidates[0].person_id
                if identifiedUniqueId not in identifiedFace :
                    identifiedFace.append(identifiedUniqueId)

                print('Person for face ID {} is identified with a confidence of {}.'.format(person.face_id, person.candidates[0].confidence)) # Get topmost confidence score
            else:
                print('No person identified for face ID {} .'.format(person.face_id))

        print("identified unique face ids : {}".format(identifiedFace))
        status=markAttendance(identifiedFace,subject)
        if status=='success':
            return jsonify(identifiedFace)
        else:
            return "error"
    except:
        i.close()
        removeTrainDataset(target)    
        return "error"


# Fetch teacher Information
def fetchTeacher():
    res = db.teachersdataset.find()
    return res

def fetchTeacherId():
    res = db.teachersdataset.find({},{'username':1})
    teachersid=[]
    for i in res:
        teachersid.append(i['username'])
    return teachersid

def fetchTeachersSubject(teacherId):
    print("Teachers Id",teacherId)
    res=db.teachersdataset.find_one({'username':teacherId},{"subject":1,'_id':0})
    subjectList=(res['subject'])
    return (subjectList)
    
