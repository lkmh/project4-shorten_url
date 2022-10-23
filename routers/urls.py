from fastapi import APIRouter, Depends, Request , HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
import base64
import re
from helper_functions.url_func import *
from sql.database import *

router = APIRouter()

@router.post('/shorten_url', status_code=200)
def shorten_url(*, long_URL: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_optional()
    # If no jwt is sent in the request, get_jwt_subject() will return None
    current_user = Authorize.get_jwt_subject() or ""

    ## check if url valid 
    if is_url_valid(long_URL) == False:
        raise HTTPException(status_code=401, detail="URL is not Valid")
    
    ## if url is a domain insert htts:
    db_url = format_url(long_URL)

    ## insert to db 

    hashed_url = urls_insert_new(db_url, userid=current_user)
    return {'shorten_url' : hashed_url}


