from flask import render_template, request, redirect, url_for, session
from flask import jsonify
from app import app
from model import *
import os

from werkzeug.utils import secure_filename


@app.route('/', methods=["GET"])
def home():

    if "username" in session:
        ch_list = fetchSubjectAttendance()
        ab_list = fetchlabelAttendance()
<<<<<<< HEAD
        ss_list = fetchTotalAttendance()

        return render_template('index.html', ch_list=ch_list, ab_list=ab_list ,ss_list=ss_list)
=======
        return render_template('index.html', ch_list=ch_list, ab_list=ab_list)
>>>>>>> d96927fc9bcfb07b100e68c277048ac41744e32f
    else:
        return render_template('login.html')



# Register new user
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":

        return render_template("register.html")
    elif request.method == "POST":
        registerUser()

        return redirect(url_for("parents_register"))

# Parents_register
@app.route('/parents_register', methods=["GET", "POST"])
def parents_register():
    return render_template("parents_register.html")

# Check if username already exists in the registratiion page
@app.route('/checkusername', methods=["POST"])
def check():
    return checkusername()

# Check if email already exists in the registratiion page
@app.route('/checkemail', methods=["POST"])
def checkem():
    return checkemail()


# Everything Login (Routes to renderpage, check if username exist and also verifypassword through Jquery AJAX request)
@app.route('/login', methods=["GET"])
def login():

    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            return redirect(url_for("home"))

# check loginusername
@app.route('/checkloginusername', methods=["POST"])
def checkUserlogin():
    return checkloginusername()

# check loginpassword
@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return checkloginpassword()

# The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    session.pop('username', None)  # remove user session
    return redirect(url_for("home"))  # redirect to home page with message

# Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')


# Cards Page
@app.route('/cards', methods=["GET"])
def cards():
    return render_template('cards.html')

# Charts Page
@app.route('/charts', methods=["GET"])
def charts():
    ch_list = fetchSubjectAttendance()
    ab_list = fetchlabelAttendance()

    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('charts.html', ch_list=ch_list, ab_list=ab_list)


# Attendance Record Page
@app.route('/tables', methods=["GET"])
def tables():
    atd_list = fetchAttendance()
    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('tables.html', atd_list=atd_list)


# Student_Information Page
@app.route('/user_info', methods=["GET","POST"])
def user_info():
    ds_list = fetchstudent()
<<<<<<< HEAD
    return render_template('user_info.html', ds_list=ds_list)
        
    # atd_list = mongo.facerecognition.attendace.find()

# Reset_Password
@app.route('/reset_password', methods=["GET"])
def reset():
    return render_template("reset_password.html")
=======
    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('user_info.html', ds_list=ds_list)   
>>>>>>> d96927fc9bcfb07b100e68c277048ac41744e32f

# 404 Page
@app.route('/404', methods=["GET"])
def errorpage():
    return render_template("404.html")

# Blank Page
@app.route('/blank', methods=["GET"])
def blank():
    return render_template('blank.html')

# Buttons Page
@app.route('/buttons', methods=["GET"])
def buttons():
    return render_template("buttons.html")

# Utilities-animation
@app.route('/utilities-animation', methods=["GET"])
def utilitiesanimation():
    return render_template("utilities-animation.html")

# Utilities-border
@app.route('/utilities-border', methods=["GET"])
def utilitiesborder():
    return render_template("utilities-border.html")

# Utilities-color
@app.route('/utilities-color', methods=["GET"])
def utilitiescolor():
    return render_template("utilities-color.html")

# utilities-other
@app.route('/utilities-other', methods=["GET"])
def utilitiesother():
    return render_template("utilities-other.html")

<<<<<<< HEAD

'''
FACE RECOGNITION START
'''
=======
>>>>>>> d96927fc9bcfb07b100e68c277048ac41744e32f
# Creating Perosn Group
@app.route('/create-person-group', methods=["GET", "POST"])
def createGroup():
    if request.method == "POST":
        print("done")
        faceclass = addGroupName()
        createPersonGroup(faceclass)
        return redirect(url_for("home"))
    return render_template("facegroup.html")


# Check group name
@app.route('/checkgroupname', methods=['POST'])
def checkgroupname():
    return checkFaceGroupName()

<<<<<<< HEAD

# Timetable Page
@app.route('/timetable', methods=["GET"])
def timetable():
    kd_list = fetchTimetable()
    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('timetable.html', kd_list=kd_list)

#Generate report
@app.route('/generatereport', methods=["GET"])
def generateReport():
    return render_template('generatereport.html')



'''
FACE RECOGNITION END
'''
=======
# timetTables Page
@app.route('/timetable', methods=["GET","POST"])
def timetable():
    kd_list = fetchTimetable()
    return render_template('timetable.html',kd_list=kd_list)



#delete button
@app.route('/delete/<string:email>', methods = ["GET","POST"])
def delete(email):
    delet(email)
    return redirect(url_for("user_info"))
    
#edit button
@app.route('/edit/<string:email>', methods = ["GET","POST"])
def edit(email):
    session['update_data'] = email
    return redirect(url_for("update"))
  
#Update values      
@app.route('/update',methods = ["GET","POST"])
def update():
    email = session.get('update_data')
    if request.method == "GET":
        users = fetchuser(email)
        return render_template('update.html',users = users)
    elif request.method == 'POST':
        updateuser(email)
        return redirect(url_for("user_info"))

#edit profile
@app.route('/editprofile/<string:uname>', methods = ["GET","POST"])
def editprofile(uname):
    session['update'] = uname
    return redirect(url_for("updateprofile"))
  
#Update profile     
@app.route('/updateprofile',methods = ["GET","POST"])
def updateprofile():
    uname = session.get('update')
    if request.method == "GET":
        users = findprofile(uname)
        return render_template('profile.html',users = users)
    elif request.method == 'POST':
        saveprofile(uname)
        return redirect(url_for("updateprofile"))

# update Password
@app.route('/reset_password', methods=["GET","POST"])
def reset_password():
    username = session.get('username')
    if request.method == "GET":
        return render_template('reset_password.html')
    elif request.method == 'POST':  
        updatepass(username)
        return redirect(url_for("user_info"))


#reset password
@app.route('/reset_pass', methods=["GET","POST"])
def reset_pass():        
    return render_template('reset_password.html')


@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=="GET":
        classroom=showClassroom()
        return render_template("student-registration.html",classroom=classroom)
    if request.method=="POST":
        studentregistration()
        return  redirect(url_for("blank"))
>>>>>>> d96927fc9bcfb07b100e68c277048ac41744e32f
