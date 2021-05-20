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

        return render_template('index.html',ch_list = ch_list,ab_list=ab_list)
    else:
        return render_template('login.html')

@app.route('/total_attendance', methods=["GET"])
def total():
    
        p_list = fetchtotalAttendance()

        return render_template('index.html',p_list=p_list)
    
# Register new user
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        
        return render_template("register.html")
    elif request.method == "POST":
        registerUser()

        return redirect(url_for("parents_register"))

#Parents_register
@app.route('/parents_register',methods=["GET","POST"])
def parents_register():
    return render_template("parents_register.html")

#Check if email already exists in the registratiion page
@app.route('/checkusername', methods=["POST"])
def check():
    return checkusername()

#Check if email already exists in the registratiion page
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



@app.route('/checkloginusername', methods=["POST"])
def checkUserlogin():
    return checkloginusername()

@app.route('/checkloginpassword', methods=["POST"])
def checkUserpassword():
    return checkloginpassword()

#The admin logout
@app.route('/logout', methods=["GET"])  # URL for logout
def logout():  # logout function
    session.pop('username', None)  # remove user session
    return redirect(url_for("home"))  # redirect to home page with message

#Forgot Password
@app.route('/forgot-password', methods=["GET"])
def forgotpassword():
    return render_template('forgot-password.html')


#Cards Page
@app.route('/cards', methods=["GET"])
def cards():
    return render_template('cards.html')

#Charts Page
@app.route('/charts', methods=["GET"])
def charts():
    ch_list = fetchSubjectAttendance()
    ab_list = fetchlabelAttendance()

    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('charts.html',ch_list = ch_list,ab_list=ab_list)


#Tables Page
@app.route('/tables', methods=["GET"])
def tables():
    atd_list = fetchAttendance()
    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('tables.html', atd_list = atd_list)

#Total_register
@app.route('/user_info', methods=["GET"])
def user_info():
    ds_list = fetchstudent()
    # atd_list = mongo.facerecognition.attendace.find()
    return render_template('user_info.html', ds_list = ds_list)

#Reset_Password
@app.route('/reset_password', methods=["GET"])
def reset():
    return render_template("reset_password.html")

#404 Page
@app.route('/404', methods=["GET"])
def errorpage():
    return render_template("404.html")

#Blank Page
@app.route('/blank', methods=["GET"])
def blank():
    return render_template('blank.html')

#Buttons Page
@app.route('/buttons', methods=["GET"])
def buttons():
    return render_template("buttons.html")

#Utilities-animation
@app.route('/utilities-animation', methods=["GET"])
def utilitiesanimation():
    return render_template("utilities-animation.html")

#Utilities-border
@app.route('/utilities-border', methods=["GET"])
def utilitiesborder():
    return render_template("utilities-border.html")

#Utilities-color
@app.route('/utilities-color', methods=["GET"])
def utilitiescolor():
    return render_template("utilities-color.html")

#utilities-other
@app.route('/utilities-other', methods=["GET"])
def utilitiesother():
    return render_template("utilities-other.html")
    




# @app.route('/upload', methods=['GET','POST'])
# def upload():
#     # f = request.files['photo']

#         # Save the file to ./uploads
#     # print("upload")
#     # basepath = os.path.dirname(__file__)
#     # file_path = os.path.join(
#     # basepath, 'upload', secure_filename(f.filename))
#     # f.save(file_path)
#     # print("Image uploaded")
#     # return render_template("register.html")
#     if request.method == 'POST':
#         return jsonify(request.form['username'], request.form['file'])
#     if request.method == 'POST':
#         file = request.files['file']
#         extension = os.path.splitext(file.filename)[1]
#         f_name = str(uuid.uuid4()) + extension
#         file.save(os.path.join('upload', f_name))
#     return json.dumps({'filename':f_name})

#hello from akshay
# hello from my own branch
#darshan

'''
FACE RECOGNITION START
'''
#Creating Perosn Group 
@app.route('/create',methods=["GET","POST"])
def createGroup():
    if request.method == "POST" :
        print("done")

        addGroupName()


        return redirect(url_for("parents_register"))
    return render_template("facegroup.html")


    
# Check group name
@app.route('/checkgroupname',methods=['POST'])
def checkgroupname():
    return checkFaceGroupName()
        





'''
FACE RECOGNITION END
'''
