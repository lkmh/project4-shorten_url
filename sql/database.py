from random import randrange
from sqlalchemy import create_engine
import hashlib
import time
import os
from dotenv import load_dotenv, find_dotenv
import bcrypt
import random

load_dotenv(find_dotenv())

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
salt = os.environ.get('SALT').encode('utf-8')
db_string = "postgresql://{}:{}@arjuna.db.elephantsql.com/{}".format(db_user, db_pass,db_user)

db = create_engine(db_string)

def hash_func_shorten_url(original_url):
    """ hash the original url to 7 """
    hash_url = hashlib.sha1(original_url.encode('utf-8')).hexdigest()[:7]
    return hash_url

def is_hash_unique(hash):
    """ check if hash is unique """
    sql_string = "SELECT * FROM urls WHERE hash_url = '{}'".format(hash)
    print(sql_string)
    data = db.execute(sql_string)
    if data is None:
        return True 
    else:
        return False
    
def get_originalurl_with_hash(hash):
    """ query for original url using the hash """
    sql_string = "SELECT original_url FROM urls WHERE hash_url = '{}'".format(hash)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    if data is None:
        return False 
    else:
        return {'original_url': data[0]}


def urls_insert_new(original_url, userid=None):
    """ insert new entry into the url db and create new hash """
    hash_url = hash_func_shorten_url(original_url)
    current_time_unix = int(time.time())

    if is_hash_unique(hash_url) != True:
        salt = bcrypt.gensalt()
        new_original_url = original_url + str(salt.decode())
        hash_url = hash_func_shorten_url(new_original_url)
    if userid:
        sql_string = "INSERT INTO urls (original_url, hash_url, created_date, userid) VALUES ('{}','{}',{}, {})".format( original_url, hash_url, current_time_unix, userid)
    else:
        sql_string = "INSERT INTO urls (original_url, hash_url, created_date) VALUES ('{}','{}',{})".format( original_url, hash_url, current_time_unix)
    print(sql_string)
    db.execute(sql_string)
    return hash_url

def urlviews_insert_new(hash_url, user_agent=None, ip_address=None):
    """ insert new entry into url views db for analytics """
    current_time_unix = int(time.time())
    sql_string = "INSERT INTO url_views (hash_url, view_date, user_agent, ip_address) VALUES ('{}', {},'{}', '{}')".format(hash_url, current_time_unix, user_agent, ip_address)
    print(sql_string)
    return db.execute(sql_string)

def hash_password(password):
    """ hashpassword in string after decoded """
    bytePwd = password.encode('utf-8')
    hashed_pw = bcrypt.hashpw(bytePwd,salt)
    hashed_pw = hashed_pw.decode('utf-8') 
    return hashed_pw


def users_insert_new(email, input_password):
    """create new user into users table"""
    current_time_unix = int(time.time())
    hashed_pw = hash_password(input_password)
    sql_string = "INSERT INTO users (email, hash_password, created_date) VALUES ('{}', '{}',{})".format(email, hashed_pw, current_time_unix)
    print(sql_string)
    return db.execute(sql_string)

def is_email_unique(email):
    """ check if email is unique """
    sql_string = "SELECT * FROM users WHERE email = '{}'".format(email)
    print(sql_string)
    data = db.execute(sql_string)
    if data is None:
        return True 
    else:
        return False

def get_userid_from(email, password):
    """ get userid after login /// noted hashing switched off """
    hashed_pw = hash_password(password)
    #hashed_pw = password
    sql_string = "SELECT id FROM users WHERE (email='{}' AND hash_password='{}')".format(email, hashed_pw)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    if data is None:
        return False 
    else:
        return int(data[0])

def get_basic_analytics(userid):
    sql_string = "SELECT urls.original_url, urls.hash_url, url_views.ip_address, url_views.user_agent, url_views.view_date, urls.userid FROM urls INNER JOIN url_views ON url_views.hash_url=urls.hash_url WHERE urls.userid={};".format(userid)
    data = db.execute(sql_string).fetchall()
    if len(data) ==0:
        return False 
    else:
        return data

def clean_all_table(tablenamelist):
    for tablename in tablenamelist:
        sql_string = "DELETE FROM {}".format(tablename)
        db.execute(sql_string)



""" DUMMY DATA USERS"""
dummary_data_users =[
                        ['a@a.com', '1'],
                        ['a2@a.com', '2'],
                        ['a3@a.com', '3'],
                        ['a4@a.com', '4'],
                        ['a5@a.com', '5'],
                        ['a6@a.com', '6'],
                        ['a7@a.com', '7'],
                    ]

def get_min_userid_users():
    sql_string = "SELECT MIN(id) FROM users"
    data = db.execute(sql_string).fetchone()
    return data[0]

def get_max_userid_users():
    sql_string = "SELECT MAX(id) FROM users"
    data = db.execute(sql_string).fetchone()
    return data[0]

db_users_start = get_min_userid_users()
db_users_end = get_max_userid_users()

# dummy_URLs = [
#                     ['https://google.com',""],
#                     ['https://digg.com', random.randint(db_users_start,db_users_end)],
#                     ['https://twitter.com',""],
#                     ['https://.com', random.randint(db_users_start,db_users_end)],
#                     ['https://medium.com/@rodrigoherrerai',""],
#                     ['https://medium.com/better-programming/uniswap-v2-in-depth-98075c826254', random.randint(db_users_start,db_users_end)],
#                     ['https://twitter.com/bertcmiller/status/1385294417091760134',""],
#                     ['https://google.com', random.randint(db_users_start,db_users_end)],
#                     ['https://twitter.com/bertcmiller/status/1385294417091760134',""],
#                     ['https://www.youtube.com/watch?v=5Vxjyz9DZ6k&t=1222s', random.randint(db_users_start,db_users_end)],
#                     ['https://www.youtube.com/watch?v=YAWX1xcLWBc',""],
#                     ['https://www.youtube.com/watch?v=70mNRClYJko', random.randint(db_users_start,db_users_end)],
#                     ['https://uniswap.org/whitepaper.pdf',""],
#                     ['https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment', random.randint(db_users_start,db_users_end)],
#                     ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/',""],
#                     ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/', random.randint(db_users_start,db_users_end)],
#                     ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/',""],
#                     ['https://google.com',""],
#                     ['https://www.youtube.com/watch?v=5Vxjyz9DZ6k&t=1222s', random.randint(db_users_start,db_users_end)],
#                 ]

# for user in dummary_data_users:
#     users_insert_new(user[0], user[1])
#     time.sleep(1)    

# hash_list = []
# for url in dummy_URLs:
#     if url[1] == "":
#         hash = urls_insert_new(url[0])
#         hash_list.append(hash)
#     else:
#         hash = urls_insert_new(url[0], url[1])
#         hash_list.append(hash)


# for hash in hash_list:
#     user_agent = ['windows', 'mac', 'ipad', 'iphone', 'mobile']
#     ip_address = str(random.randint(100,999)) + '.'+str(random.randint(100,999))+'.'+ str(random.randint(100,999))
#     urlviews_insert_new(hash, user_agent[random.randint(1,5)-1], ip_address)