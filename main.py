from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from routers.users import router as users_router
from routers.urls import router as urls_router
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

whitelist_IP = os.environ.get('WHITELIST')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://127.0.0.1:8000"], ##
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Access-Control-Allow-Origin"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
  authjwt_secret_key: str = "secret" ### to change 
  # Configure application to store and get JWT from cookies
  authjwt_token_location: set = {"cookies"}
  # Disable CSRF Protection for this example. default is True
  authjwt_cookie_csrf_protect: bool = False
  authjwt_cookie_samesite: str = "none"
  authjwt_cookie_secure: bool = True
  authjwt_access_token_expires: int = 10

# callback to get your configuration
@AuthJWT.load_config
def get_config():
  return Settings()


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
  return JSONResponse(status_code=exc.status_code,
                      content={"detail": exc.message})


app.include_router(users_router, tags=['users'])
app.include_router(urls_router, tags=['urls'])

