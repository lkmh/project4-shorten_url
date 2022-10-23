from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from operator import is_
from dotenv import load_dotenv, find_dotenv
from sql.database import *
from helper_functions.validation_func import *

class User(BaseModel):
  email: str
  password: str


router = APIRouter()

@router.post('/v1/signup')
def login(user: User):
    ## check if email is valid
    if is_Email_valid(user.email) == False:
      raise HTTPException(status_code=401, detail="Bad email") ## in product change to Bad email/password
    ## check if email is unique 
    if is_email_unique(user.email) == False:
      raise HTTPException(status_code=401, detail="Email used before")
    ## check if password is ok 
    if is_Password_valid(user.password) == False:
      raise HTTPException(status_code=401, detail="Password not valid")
    ## create new user 
    users_insert_new(user.email, user.password)
    return {"msg": "Successfully Signup"}

# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@router.post('/v1/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    response = get_userid_from(user.email, user.password)
    print(response)
    if response == False:
        raise HTTPException(status_code=401, detail="Bad username or password")
    else:
    # subject identifier for who this token is for example id or username from database
        access_token = Authorize.create_access_token(subject=response)
        Authorize.set_access_cookies(access_token)
        return {"msg": "Successfully login"}


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@router.get('/v1/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@router.delete('/v1/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
      Because the JWT are stored in an httponly cookie now, we cannot
      log the user out by simply deleting the cookies in the frontend.
      We need the backend to send us a response to delete the cookies.
      """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}


# @router.get('/v1/partially-protected')
# def partially_protected(Authorize: AuthJWT = Depends()):
#       Authorize.jwt_optional()

#       # If no jwt is sent in the request, get_jwt_subject() will return None
#       current_user = Authorize.get_jwt_subject() or "anonymous"
#       return {"user": current_user}