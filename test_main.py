from fastapi.testclient import TestClient
from sql.database import *
from .main import app
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

login_email = os.environ.get('user')
login_password = os.environ.get('password')
login_userid = os.environ.get('userid')

client = TestClient(app)


""" Step 1 """

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

""" Step 2 - DB setup  """

# def test_maxusers_fromDB_main():
#     response = get_max_userid_users()
#     assert response == 7

def test_get_original_url_with_hash():
    response = get_originalurl_with_hash("3066553")
    assert response ==  {"original_url": "https://google.com"}

def test_collision_with_existing_hash():
    """original_url = htts://google.com"""
    existing_hash_for_google = "3066553"
    response =  urls_insert_new("htts://google.com")
    assert response != "3066553"

""" Step 3 - users auth - login and get user """

params_login_main =  json.dumps({
            'email': login_email,
            'password': login_password
        })

def test_login_main():
    response = client.post("/login", data=params_login_main)
    assert response.status_code == 200
    assert response.json() == {"msg": "Successfully login"}

params_user_main =  json.dumps({
            'email': login_email,
            'password': login_password
        })
def test_user_main():
    response = client.post("/login", data=params_user_main)
    response = client.get("/user", cookies=response.cookies)
    assert response.status_code == 200
    assert response.json() == {"user": int(login_userid)}

""" Step 3 --- users sign up """


params_signup_existing_main =  json.dumps({
            'email': login_email,
            'password': 'A12801@1a'
        })

def test_signup_existing_main():
    response = client.post("/signup", data=params_signup_existing_main)
    assert response.status_code == 401
    assert response.json() == {"detail": "Email used before"}

params_signup_bademail_main =  json.dumps({
            'email': '2A.com',
            'password': login_password
        })

def test_signup_bademail_main():
    response = client.post("/signup", data=params_signup_bademail_main)
    assert response.status_code == 401
    assert response.json() == { "detail": "Bad email"}

params_signup_badpassword_main =  json.dumps({
            'email': 'asdjkasd@A.com',
            'password': '1'
        })

def test_signup_badpassword_main():
    response = client.post("/signup", data=params_signup_badpassword_main)
    assert response.status_code == 401
    assert response.json() == {"detail": "Password not valid"}



