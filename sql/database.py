from random import randrange
import hashlib
import time
import bcrypt
from helper_functions.url_func import *
from helper_functions.user_func import *
from sql.connect_db import *
import json

""" For URL """

def is_hash_unique(hash):
    """ check if hash is unique """
    sql_string = "SELECT * FROM urls WHERE hash_url = '{}'".format(hash)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    print("data",data)
    if data is None:
        return True ## is NONE =>> hash not used before 
    else:
        return False ## å=>> hash  used before 

def get_originalurl_with_hash(hash):
    """ query for original url using the hash """
    sql_string = "SELECT original_url FROM urls WHERE hash_url = '{}'".format(hash)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    if data is None:
        return False 
    else:
        return {'original_url': data[0]}

def get_userid_with_hash(hash):
    """ query for original url using the hash """
    sql_string = "SELECT userid FROM urls WHERE hash_url = '{}'".format(hash)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    if data is None:
        return False 
    else:
        return {'userid': data[0]}

def urls_insert_new(original_url, userid=None):
    """ insert new entry into the url db and create new hash """
    hash_url = hash_func_shorten_url(original_url)
    current_time_unix = int(time.time())

    if is_hash_unique(hash_url) != True:
        salt = bcrypt.gensalt()
        new_original_url = original_url + str(salt.decode())
        hash_url = hash_func_shorten_url(new_original_url)
    if userid :
        sql_string = "INSERT INTO urls (original_url, hash_url, created_date, userid) VALUES ('{}','{}',{}, {})".format( original_url, hash_url, current_time_unix, userid)
    else:
        sql_string = "INSERT INTO urls (original_url, hash_url, created_date) VALUES ('{}','{}',{})".format( original_url, hash_url, current_time_unix)
    print(sql_string)
    db.execute(sql_string)
    return hash_url


""" for URL Views """

def urlviews_insert_new(hash_url, user_agent=None, ip_address=None):
    """ insert new entry into url views db for analytics """
    current_time_unix = int(time.time())
    sql_string = "INSERT INTO url_views (hash_url, view_date, user_agent, ip_address) VALUES ('{}', {},'{}', '{}')".format(hash_url, current_time_unix, user_agent, ip_address)
    print(sql_string)
    return db.execute(sql_string)


def get_basic_analytics(userid):
    sql_string = 'SELECT urls.hash_url, COUNT(url_views.ip_address) AS "total_view_count", urls.original_url FROM urls INNER JOIN url_views ON url_views.hash_url=urls.hash_url WHERE urls.userid={} GROUP BY urls.hash_url, urls.original_url;'.format(userid)
    data = db.execute(sql_string).fetchall()
    if len(data) ==0:
        return False 
    else:
        dict_row = [row._asdict() for row in data ]
        print("dicttype", type(dict_row))
        final = json.dumps(dict_row, indent=1)
        final = json.loads(final)
        print("final type",type(final))
        print("final",final)
        return final

""" for users """

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
    data = db.execute(sql_string).fetchone()
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
def get_password_from(userid):
    sql_string = "SELECT hash_password FROM users WHERE id='{}'".format(userid)
    print(sql_string)
    data = db.execute(sql_string).fetchone()
    if data is None:
        return False 
    else:
        return (data[0])

def update_password(userid, new_password):
    sql_string = "UPDATE users SET hash_password = '{}' WHERE id='{}'".format(new_password, userid)
    print(sql_string)
    data = db.execute(sql_string)
    if data is None:
        return False 
    else:
        return (data)

""" admin """
def clean_all_table(tablenamelist):
    for tablename in tablenamelist:
        sql_string = "DELETE FROM {}".format(tablename)
        db.execute(sql_string)

