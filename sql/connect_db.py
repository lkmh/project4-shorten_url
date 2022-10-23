import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine

load_dotenv(find_dotenv())

db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASS')
salt = os.environ.get('SALT').encode('utf-8')
db_string = "postgresql://{}:{}@arjuna.db.elephantsql.com/{}".format(db_user, db_pass,db_user)

db = create_engine(db_string)
