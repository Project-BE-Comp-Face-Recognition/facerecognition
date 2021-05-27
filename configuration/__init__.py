from app import app
import urllib
import os
from dotenv import load_dotenv
load_dotenv()

# secret key for user session
app.secret_key = "ITSASECRET"

#setting up mail
app.config['MAIL_SERVER']='smtp.gmail.com' #mail server
app.config['MAIL_PORT'] = 465 #mail port
app.config['MAIL_USERNAME'] = 'ghrietcodeshef@gmail.com' #email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') #password
app.config['MAIL_USE_TLS'] = False #security type
app.config['MAIL_USE_SSL'] = True #security type

#database connection parameters
connection_params = {
    'user': 'admin',
    'password': os.environ.get('DB_PASSWORD'),
    'host': 'cluster0.vcs37.mongodb.net',
    'namespace': 'facerecognition',
}
