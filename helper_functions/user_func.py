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
