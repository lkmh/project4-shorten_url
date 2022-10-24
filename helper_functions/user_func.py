import os
from dotenv import load_dotenv, find_dotenv
import bcrypt

load_dotenv(find_dotenv())
salt = os.environ.get('SALT').encode('utf-8')

def hash_password(password):
    """ hashpassword in string after decoded """
    bytePwd = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(bytePwd,salt)
    hashed_pw = hashed_pw.decode('utf-8') 
    return hashed_pw

load_dotenv(find_dotenv())

db_emailer_username = os.environ.get('emailer_username')
db_emailer_password = os.environ.get('emailer_password')

import smtplib, ssl

def send_reset_password(receiver_email, temp_hash):
    port = 587  # For starttls
    smtp_server = "smtp-mail.outlook.com"
    sender_email = db_emailer_username
    receiver_email =receiver_email
    password =  db_emailer_password
    message = """\
    Subject: Reset Password

    Input this hash {} to reset password """.format(str(temp_hash))

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return True 