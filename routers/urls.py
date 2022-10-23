from fastapi import APIRouter, Depends, Request , HTTPException
from fastapi_jwt_auth import AuthJWT
from fastapi.responses import RedirectResponse
import base64
import re
from helper_functions.url_func import *
from sql.database import *

router = APIRouter()

@router.post('/v1/shorten_url', status_code=200)
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


@router.get("/{short_URL}", response_class=RedirectResponse)
async def redirect_fastapi(*, short_URL: str, request: Request):
    if is_hash_unique(short_URL) == True :
        raise HTTPException(status_code=401, detail="Short URL is not Valid")
    user_agent = request.headers['user-agent']
    print('USER AGENT',user_agent)
    client_ip = request.client.host
    clean_client_ip = clean_ip(client_ip)
    print('RAW USER IP',client_ip)
    print('Clean USER IP',clean_client_ip)
    website = get_originalurl_with_hash(short_URL)['original_url']
    print('WEBSITE', website)
    urlviews_insert_new(short_URL, user_agent, clean_client_ip)
    return website  ### without the http:// got problem

@router.get('/v1/analytics')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    data = get_basic_analytics(current_user)
    return {'data':data}