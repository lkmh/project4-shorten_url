from random import randrange
from sqlalchemy import create_engine
import hashlib
import time
import os
from dotenv import load_dotenv, find_dotenv
import bcrypt
from sql.database import *
import random




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

db_users_start =get_max_userid_users()+ 1
db_users_end = get_max_userid_users()+ 1 + 7

dummy_URLs = [
                    ['https://google.com',""],
                    ['https://digg.com', random.randint(db_users_start,db_users_end)],
                    ['https://twitter.com',""],
                    ['https://.com', random.randint(db_users_start,db_users_end)],
                    ['https://medium.com/@rodrigoherrerai',""],
                    ['https://medium.com/better-programming/uniswap-v2-in-depth-98075c826254', random.randint(db_users_start,db_users_end)],
                    ['https://twitter.com/bertcmiller/status/1385294417091760134',""],
                    ['https://google.com', random.randint(db_users_start,db_users_end)],
                    ['https://twitter.com/bertcmiller/status/1385294417091760134',""],
                    ['https://www.youtube.com/watch?v=5Vxjyz9DZ6k&t=1222s', random.randint(db_users_start,db_users_end)],
                    ['https://www.youtube.com/watch?v=YAWX1xcLWBc',""],
                    ['https://www.youtube.com/watch?v=70mNRClYJko', random.randint(db_users_start,db_users_end)],
                    ['https://uniswap.org/whitepaper.pdf',""],
                    ['https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment', random.randint(db_users_start,db_users_end)],
                    ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/',""],
                    ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/', random.randint(db_users_start,db_users_end)],
                    ['https://www.geeksforgeeks.org/how-to-hash-passwords-in-python/',""],
                    ['https://google.com',""],
                    ['https://www.youtube.com/watch?v=5Vxjyz9DZ6k&t=1222s', random.randint(db_users_start,db_users_end)],
                ]

for user in dummary_data_users:
    users_insert_new(user[0], user[1])
    time.sleep(1)    

hash_list = []
for url in dummy_URLs:
    if url[1] == "":
        hash = urls_insert_new(url[0])
        hash_list.append(hash)
    else:
        hash = urls_insert_new(url[0], url[1])
        hash_list.append(hash)


for hash in hash_list:
    user_agent = ['windows', 'mac', 'ipad', 'iphone', 'mobile']
    ip_address = str(random.randint(100,999)) + '.'+str(random.randint(100,999))+'.'+ str(random.randint(100,999))
    urlviews_insert_new(hash, user_agent[random.randint(1,5)-1], ip_address)