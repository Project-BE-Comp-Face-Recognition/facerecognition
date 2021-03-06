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
from datetime import date , timedelta ,datetime
import time
import pandas as pd
import numpy as np



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


def fetchAttendance(classroom,sdate,edate):
    diff = []
    if edate == None and sdate == None :
        edate = date.today()
        sdate = edate - timedelta(days = 30)
    
    elif edate == '' or sdate == '':
        if sdate == '':
            if edate == '':
                edate = date.today()
                sdate = (edate - timedelta(days= 30))
            else :
                sd = datetime.strptime(edate, '%Y-%m-%d').date()
                sdate = (sd - timedelta(days= 30))
        else:
            edate = date.today() 
                
    sdate=str(sdate)
    edate=str(edate)        
    diff.append(sdate)
    diff.append(edate)
    diff.append(datediff(sdate,edate))
    res=db.syllabus.find_one({'classroom':classroom},{"subject":1,"_id":0})
    sub=res['subject']
    group={
            "$group": {
                "_id": "$_id",
                "rollnumber": {"$first": '$rollnumber'},
                "name": {"$first": '$name'},
                "classroom": {"$first": '$classroom'},
                "personId": {"$first": '$personId'}
            }
        }

    for i in sub:
        a={i:{"$sum":"$attendance.todaysattendance."+i}}
        group["$group"].update(a)
        


    r=db.attendancelog.aggregate([
        {
            "$unwind": "$attendance",
            
        },
        {
            "$match":{
                "attendance.date":{"$gte":sdate, "$lte":edate}
            }
        },
        {
        "$project": {
                "attendance":1,
                "name":1,
                "rollnumber":1,
                "classroom":1,
                "personId" :1    
            }
        }
        ,
        group
        
    ])

    res=list(r)
    return sub,res,diff



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
                "attendance.date":{"$gte":i, "$lt":str(today)}
            },{
                "_id":1
            }))
        cardValue.append(len(value))
    chartData=dict(zip(cardKey,cardValue))
    return chartData



# Fetch Student Information
def fetchstudent():
    res = db.studentdataset.find()
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
# def delet(uname):
#     db.studentdataset.remove({"username" : uname})
    
#Edit button
def fetchuser(uname):
    users = db.studentdataset.find_one({"username":uname})
    return users



def updateuser(uname):
    name = request.form['name']
    classroom = request.form['classroom']
    rollnumber = request.form['rollnumber']
    mobile = request.form['mobile']
    parentname = request.form['parentname']
    parentemail = request.form['parentemail']
    parentmobile = request.form['parentmobile']
    db.studentdataset.update({"username": uname},
                   {"$set": {
                      "name" : name,
                      "classroom" : classroom,
                      "rollnumber" : rollnumber,
                      "mobile" : mobile,
                      "parentname" : parentname,
                      "parentemail" : parentemail,
                      "parentmobile" : parentmobile}})
  


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
    modified=0
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
            db.attendancelog.update_one({'personId':i},{'$push':{"attendance":{"$each":[attendance] ,"$position":0}}})
            modified+=res.modified_count
            print(modified)

    if modified!=0:        
        return "success"
    else :
        return None



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
    

def piedata():
    # Get today's date
    today = date.today()
    # Yesterday date
    yesterday = str(today - timedelta(days = 1))
    key=showClassroom()
    value=[] 
    for classs in key:

        res=list(db.attendancelog.find(
            {"attendance.date":yesterday ,"classroom":classs},{"_id":1}
        ))  
        value.append(len(res))

    return key,value
        
def bardata():
    # Get today's date
    today = date.today() 
    # Yesterday date
    yesterday = str(today - timedelta(days = 1))
    key=showClassroom()
    label=[yesterday]
    value=[] 
    for classs in key:

        res=list(db.attendancelog.find(
            {"attendance.date":yesterday ,"classroom":classs},{"_id":1}
        ))  
        value.append(len(res))
    return key,value,label
        


#Fetch syllabus
def fetchSyllabus(classroom):
    if classroom == None:
        classroom = session.get('clasroom')
    li = db.syllabus.find_one({"classroom" : classroom})
    syllabus = li['subject']
    return syllabus

def areaChart():

    today = date.today()
    day1 = str(today - timedelta(days = 7))
    day2 = str(today - timedelta(days = 6))
    day3 = str(today - timedelta(days = 5))
    day4 = str(today - timedelta(days = 4))
    day5 = str(today - timedelta(days = 3))
    day6 = str(today - timedelta(days = 2))
    day7 = str(today - timedelta(days = 1))
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
            if value != None:
                subjects.append(value) 
    db.syllabus.update_one({"classroom" : classname},{ '$set' : { "subject": subjects } }
                           )

#List to string converter
def convertToString(atd_list,sdate,edate):
    csv =''   # initializing the empty string
    count =0
    diff = datediff(sdate,edate)
    for atd in atd_list[1]:
        del atd["_id"]
        del atd["name"]
        res = db.studentdataset.find_one({'personId': atd['personId']},{"_id":0,"username":1,"name":1,"email":1,"parentname":1,"parentemail":1})
        del atd["personId"]
        key2 = res.keys()
        key1 = atd.keys() 
        value2 = res.values() 
        value1 = atd.values()
        keys = list(key2) + list(key1)
        values = list(value2) + list(value1)
        if count == 0 :         
            for i in keys:                      
                csv += i+","  
            csv += "Average(%)"           
        csv += "\n"
        avg = 0
        for j in values:
            csv += str(j)+","
            count += 1  
            if type(j) == int :
                avg += j
        csv += str(round((avg*100)/(6*diff),2))    
    mailData(csv)
    return csv  

#Find Single Teacher Usinh Username
def findTeacher(uname):
    res = db.teachersdataset.find({'username':uname})
    for t in res:    
        return t    

def updatTeacher(uname) :
    name = request.form["name"]
    number = request.form["number"]
    classroom = request.form["classroom"]
    subjects = request.form.getlist('subject[]')
    subject = [i for i in subjects if i]
    db.teachersdataset.update_one({"username": uname},
                   {"$set": {
                      "name" : name,
                      "number" : number,
                      "classroom" : classroom,
                      "subject" : subject}})
    
# Date difference Calculator
def datediff(date1,date2):
    
    d1 = pd.to_datetime(date1,format = '%Y-%m-%d').date()
    d2 = pd.to_datetime(date2,format = '%Y-%m-%d').date()
    diff = np.busday_count(d1,d2) + 1
    # days = np.busday_count( start, end,holidays=[holidays] )        Incaseyou want to provide holiday
    return diff

def mailData(csv):
    lst=csv.splitlines()
    for i in lst[1:]:
        a=i.split(",")
        
        studentname = a[0]
        studentemail = a[2] 
        parentsname = a[3]
        parentsemail = a[4]   
        classname = a[6] 
        avgattendance= float(a[len(a)-1])
        mdate = str(date.today())
           
        subject = "Student Attendance Report   - No Reply"
        recipients = studentemail
        sender = app.config["MAIL_USERNAME"]
        
        # h = []
        # v = []
        # b = lst[0].split(",")
        # for i in range(7,len(a)):
        #     v.append(a[i])
        #     h.append(b[i])    
        # table  = [h,v]
        # mark = tabulate(table, headers='firstrow', tablefmt='fancy_grid')
        
        if avgattendance <= 35.00 :        
            body = mdate+"\n"+parentsname+"\n"+parentsemail+"\nDear Sir,\n\nWe regret to inform you that your son/daughter "+studentname+" is a student of "+classname+" in G.H.Raisoni Institute of Engineering & Technology , Wagholi. It has been an awful situation to inform you about his/her recent educational record. He/she has not been present in his/her classes most of the time. It is noted that he/she is having a below average attendance to attempt the final year exams that are to be held this season. Every teacher individually warned him/her of his present condition but they have failed to change his/her mind to attend classes on regular basis. So we are only left with the last option to inform you about his/her situation. You are being his guardian can handle this situation more effectively now. So we will leave this problem to you from now on.\n     Apart from the above-mentioned attendance problem, there is another attitude problem is being observed in your son/daughter. He/she has been observed behaving badly with most of his/her teachers. Keeping in view his/her old records we did not expel him/her just yet. We have warned him/her and given him/her another chance to be a good lad in our school and we felt it essential to inform you also so that you can make him/her stop ruin his/her education and life. As the teachers and management are not happy with him/her we are issuing this warning letter so that he can continue his/her studies in a disciplined way that every other student follows here.\n\n       We are looking forward to an intense action from you. So it would really be appreciated by us.\n\nThanking you.\nYours Truly,\n Dr. Nilesh Deotale \n       HOD"
        
        elif avgattendance > 35.00 and avgattendance <= 50.00 :
            body = mdate+"\n"+parentsname+"\n"+parentsemail+"\n\nDear Sir,\nWe regret to inform you that your son/daughter "+studentname+" is a student of "+classname+" in G.H.Raisoni Institute of Engineering & Technology , Wagholi. It has been a worrying situation to inform you about his/her recent educational record. He/she has not been present in his/her classes regularly. It is noted that he/she is having an average attendance to attempt the final year exams that are to be held this season. Every teacher individually told him/her of his present condition but they have failed to change his/her mind to attend classes on regular basis. So we are only left with the last option to inform you about his/her situation. You are being his guardian can handle this situation more effectively now. So we will leave this problem to you from now on.\n       Keeping in view his old records we did not expel him/her just yet. We have warned him and given him another chance to be a good lad in our school and we felt it essential to inform you also so that you can make him/her stop ruin his education and life. As the teachers and management are happy with him/her academic performance. we are issuing this warning letter so that he can continue his studies in a disciplined way that every other student follows here.\nWe are looking forward to an intense action from you. So it would really be appreciated by us.\nThanking you.\nYours Truly,\n Dr. Nilesh Deotale \n      HOD"            
        
        elif avgattendance > 50.00 :
            body = mdate+"\n"+parentsname+"\n"+parentsemail+"\n\nDear Sir,\nWe happy to inform you that your son/daughter "+studentname+" is a student of "+classname+" in G.H.Raisoni Institute of Engineering & Technology , Wagholi. It has been an excellent situation to inform you about his/her recent educational record. He/she has present in his/her classes most of the time. It is noted that he/she is having a excellent attendance to attempt the final year exams that are to be held this season. Every teacher individually awarded him of his present condition. So we are very happy to inform you about his/her performance. You are being his/her guardian can proud on him/her.\n\n      We believe if he/she continues his/her co-orporation in this way might see agood progress in his/her grades in upcoming exams. He/She is interactive and focused towards his/her studies. He/She just need to consistant with his/her attendance.  \n\n     We are glad to have him/her in our college. \n\nThanking you.\nYours Truly,\n Dr. Nilesh Deotale \n    HOD"
        recipt = sendmail(subject,sender,recipients,body)
        print(recipt," for ",studentemail)
    
        

