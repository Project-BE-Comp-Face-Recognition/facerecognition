from flask.json import jsonify
from app import app
from flask import request, session
from helpers.database import *
from helpers.hashpass import *
from helpers.mailer import *
from helpers.recognition import *
from helpers.path import *
from helpers.facecrop import *
from bson import json_util, ObjectId
import json,shutil
from datetime import date , timedelta
import time


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




def fetchAttendance(classroom):
    res=db.syllabus.find_one({'classroom':classroom},{"subject":1,"_id":0})
    sub=res['subject']
    group={
            "$group": {
                "_id": "$_id",
                "name": {"$first": '$name'},
                "rollnumber": {"$first": '$rollnumber'},
                "classroom": {"$first": '$classroom'},
            }
        }

    for i in sub:
        a={i:{"$sum":"$attendance.todaysattendance."+i}}
        group["$group"].update(a)

    pipe = [
        {"$match": {
            "attendance.date": "2021-06-04",
            "classroom":classroom
        }
        },
        {
            "$unwind": "$attendance"
        },
        group
    ]

    res= list(db.attendancelog.aggregate(pipe))
    print(res)
    
    '''
    old
    '''
    # res = db.attendance.find()    
    return sub,res



#fetch total attendance
def fetchTotalAttendance():
    today = date.today()
    yesterday = str(today - timedelta(days = 1))
    lastweek = str(today - timedelta(days = 7))
    lastfifteendays = str(today - timedelta(days = 15))
    lastmonth = str(today - timedelta(days = 30))
    cardKey=["yesterday","lastweek","lastfifteen","lastmonth"]
    cardValue=[]
    days=[yesterday , lastweek , lastfifteendays , lastmonth]
    for i in days:
        value= list(db.attendancelog.find({
                "attendance.date":{"$gte":i, "$lte":str(today)}
            },{
                "_id":1
            }))
        cardValue.append(len(value))
    chartData=dict(zip(cardKey,cardValue))
    return chartData



# Fetch Student Information
def fetchstudent():
    res = db.users.find()
    return res



    
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
    session['clasroom'] = clasroom
    res=list(db.timetable.aggregate([
    {"$match":{
        "class.classroom":clasroom
    }},
    {"$unwind":"$class"},
    {"$unwind":"$class.timetable"},
    { "$match": {
        "class.classroom": clasroom}}
    ]))
    tt = []
    ftt = res[0]['class']['timetable']
    tt.append(ftt)
    return tt
    



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
    dateToday= date.today().isoformat()
    for i in identifiedFace:
        try:
            res=db.attendancelog.update_one({'personId':i, "attendance.date":dateToday} , {"$inc":{"attendance.$.todaysattendance."+subjectname:1}})
        except:
            print("Error while Updating Person ID")
            return None
        modified=res.modified_count
        if modified==0:
            ta={subjectname:1}
            k=["date","todaysattendance"]
            v=[dateToday,ta]
            attendance=dict(zip(k,v))
            print(attendance)
            db.attendancelog.update_one({'personId':i},{'$push':{"attendance":attendance}})
            return "success"

        
    return "success"




def identifyFace():

    classroom=request.form['classroom']
    teachersId=request.form['teachersId']
    subject=request.form['subject']

    h=str(home)
    target = os.path.join(h, "identify")
    if not os.path.isdir(target):
        os.mkdir(target)
    teacherfolder = os.path.join(target, teachersId+"/")
    if not os.path.isdir(teacherfolder):
        os.mkdir(teacherfolder)
    for file in request.files.getlist("files[]"):
        filename = file.filename
        destination = "/".join([teacherfolder, filename])
        file.save(destination)

    teacherfolder=faceDetector(teachersId)

    imageName=[filename for filename in os.listdir(teacherfolder) ]
    print(imageName)
    face_ids = []
    identifiedFace=[]

    for image in imageName:
        i = open(teacherfolder+'/'+image, 'r+b')
        print("Fetching Face Ids ../")
        faces = face_client.face.detect_with_stream(i, detection_model='detection_03')
        if len(faces) == 1 :
            print(faces[0].face_id)
            face_ids.append(faces[0].face_id)
            time.sleep(5)
        else:
            pass
        
    i.close()
    print(target)
    print()
    print(teacherfolder)
    print()
    removeTrainDataset(target)        
    removeTrainDataset(teacherfolder)
    print("Identified face Ids From Upload-->",face_ids)
    chunks = [face_ids[x:x+10] for x in range(0, len(face_ids), 10)]
    results=[]
    try:
        for i in chunks:
            res= face_client.face.identify(i, classroom)
            results.append(res)
            print("Printing",res)
        if not results:
            print('No person identified in the person group for faces from {}.'.format(imageName))
            return 0
        print("Finding Person ID")
        for persons in results:
            for person in persons:
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
        removeTrainDataset(teacherfolder)    
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

#find Timetable
def findTimetable(day):
    clasroom = session.get('clasroom')
    res=list(db.timetable.aggregate([
    {"$match":{
        "class.classroom":clasroom
    }},
    {"$unwind":"$class"},
    {"$unwind":"$class.timetable"},
    { "$match": {
        "class.classroom": clasroom}}
    ]))
    tt = []
    ftt = res[0]['class']['timetable'][day]
    tt.append(ftt)
    return tt
    
#Update Timetable
def updateTimetable(day):
    clasroom = session.get('clasroom')
    key = [k for k in request.form]                                      
    val = [request.form[k] for k in request.form] 
    data = dict(zip(key, val))
    for time,subject in data.items():      
        db.timetable.update_one({'class.classroom':clasroom},{'$set':{"class.$.timetable."+day+"."+time:subject}})
    
#Fetch syllabus
def fetchSyllabus(classroom):
    if classroom == None:
        classroom = session.get('clasroom')
    li = db.syllabus.find_one({"classroom" : classroom})
    syllabus = li['subject']
    return syllabus


def areaChart():
    today = date.today()
    day1 = str(today - timedelta(days = 1))
    day2 = str(today - timedelta(days = 2))
    day3 = str(today - timedelta(days = 3))
    day4 = str(today - timedelta(days = 4))
    day5 = str(today - timedelta(days = 5))
    day6 = str(today - timedelta(days = 6))
    day7 = str(today - timedelta(days = 7))
    areaKey=[day1,day2,day3,day4,day5,day6,day7]
    areaValue=[]
    for i in areaKey:
        value= list(db.attendancelog.find({
                "attendance.date":i
            },{
                "_id":1
            }))
        areaValue.append(len(value))

    return  (areaKey,areaValue)
     
#Update Syllabus
def updatSyllabus(classname):
    subjects = []
    f = request.form
    for key in f.keys():
        for value in f.getlist(key):
            subjects.append(value) 
    db.syllabus.update_one({"classroom" : classname},{ '$set' : { "subject": subjects } }
                           )
    

            