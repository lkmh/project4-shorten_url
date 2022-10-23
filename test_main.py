from fastapi.testclient import TestClient
from sql.database import *
from .main import app

client = TestClient(app)


""" Step 1 """
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

""" Step 2 - DB setup  """

def test_maxusers_fromDB_main():
    response = get_max_userid_users()
    assert response == 7

def test_get_original_url_with_hash():
    response = get_originalurl_with_hash("3066553")
    assert response ==  {"original_url": "https://google.com"}

def test_collision_with_existing_hash():
    """original_url = htts://google.com"""
    existing_hash_for_google = "3066553"
    response =  urls_insert_new("htts://google.com")
    assert response != "3066553"