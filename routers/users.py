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
def signup(user: User):
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
        access_token = Authorize.create_access_token(subject=response, expires_time=10)
        refresh_token = Authorize.create_refresh_token(subject=response)
        Authorize.set_access_cookies(access_token, max_age=60)
        Authorize.set_refresh_cookies(refresh_token, max_age=60*60*24*30)
        return {"msg": "Successfully login"}


# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@router.get('/v1/user')
def user(Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token, max_age=60)
    return {"user": current_user}

@router.patch('/v1/change_password')
def change_password(old_password :str , new_password :str, Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    hashed_old_password = hash_password(old_password)
    print("hashed_old_password", hashed_old_password)
    get_current_hashed_password = get_password_from_id(current_user)
    print('current password', get_current_hashed_password)
    hashed_new_password = hash_password(new_password)
    if hashed_old_password != get_current_hashed_password:
      raise HTTPException(status_code=401, detail="Old password is wrong")

    ## create new user 
    elif hashed_new_password == get_current_hashed_password:
      raise HTTPException(status_code=401, detail="New password cannot match old password")
    elif is_Password_valid(new_password) == False:
      raise HTTPException(status_code=401, detail="Password not valid")
    else:
      update_password(current_user, hashed_new_password)
      Authorize.unset_jwt_cookies()
      # new_access_token = Authorize.create_access_token(subject=current_user)
      # Authorize.set_access_cookies(new_access_token, max_age=60)
      
      refresh_token = Authorize.create_refresh_token(subject=current_user)
      Authorize.set_refresh_cookies(refresh_token, max_age=60*60*24*30)
      return {"msg": 'Password Changed Successfully'}

@router.delete('/v1/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
      Because the JWT are stored in an httponly cookie now, we cannot
      log the user out by simply deleting the cookies in the frontend.
      We need the backend to send us a response to delete the cookies.
      """
    # Authorize.jwt_required()
    Authorize.jwt_refresh_token_required()

    Authorize.unset_jwt_cookies()
    return {"msg": "Successfully logout"}

@router.post('/v1/forget_password_step1')
def forget_password_step1(email: str):
    ## check if email is valid
    if is_Email_valid(email) == False:
      raise HTTPException(status_code=200, detail="We will be sending you a temp password to reset password if email is valid")
    ## check if email is unique 
    if is_email_unique(email) == True:
      raise HTTPException(status_code=200, detail="We will be sending you a temp password to reset password if email is valid")
    temp_hash = get_password_from(email)[10:16]
    send_reset_password(email, temp_hash)
    return {"detail": "We will be sending you a temp password to reset password if email is valid"}

@router.patch('/v1/forget_password_step2')
def forget_password_step2(temp_hash :str , email: str, new_password :str):
    if is_email_unique(email) == True:
      raise HTTPException(status_code=200, detail="Please input correct email and hash")
    original_forget_hash = get_password_from(email)[10:16]
    if temp_hash != original_forget_hash:
      raise HTTPException(status_code=200, detail="Please input correct email and hash")
    if is_Password_valid(new_password) == False:
      raise HTTPException(status_code=401, detail="New Password invalid")
    hashed_new_password = hash_password(new_password)
    update_password_with_email(email, hashed_new_password)
    return {"msg": 'Password Changed Successfully'}


# @router.get('/v1/partially-protected')
# def partially_protected(Authorize: AuthJWT = Depends()):
#       Authorize.jwt_optional()

#       # If no jwt is sent in the request, get_jwt_subject() will return None
#       current_user = Authorize.get_jwt_subject() or "anonymous"
#       return {"user": current_user}