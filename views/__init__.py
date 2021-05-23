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
        ss_list = fetchTotalAttendance()

        return render_template('index.html', ch_list=ch_list, ab_list=ab_list ,ss_list=ss_list)
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
    return render_template('user_info.html', ds_list=ds_list)
        
    # atd_list = mongo.facerecognition.attendace.find()

# Reset_Password
@app.route('/reset_password', methods=["GET"])
def reset():
    return render_template("reset_password.html")

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


'''
FACE RECOGNITION START
'''
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
