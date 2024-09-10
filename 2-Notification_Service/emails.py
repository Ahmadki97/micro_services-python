from parameters import * 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib






def activationMail(user):
    msg = MIMEMultipart()
    msg['from'] = sender_email
    msg['to'] = user['email']
    msg['subject'] = "Account Validation"
    message = " Hello Dear 'user[username]' Kindly Validate Your Account"
    msg.attach(MIMEText(message, 'plain'))

    # Create SMTP Session 

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)