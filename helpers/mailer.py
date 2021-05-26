from flask_mail import Mail, Message
import smtplib, ssl
from app import app
import configuration


mail = Mail(app)
def sendmail(subject, sender, receiver, body):
    try:
        msg = Message(subject, sender=sender, recipients=[receiver])
        msg.body = body
        mail.send(msg)
        return "Sent"
    except Exception as e:
        return e