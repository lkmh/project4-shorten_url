from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from routers.users import router as users_router
from routers.urls import router as urls_router
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# in production you can use Settings management
# from pydantic to get secret key from .env
class Settings(BaseModel):
  authjwt_secret_key: str = "secret"
  # Configure application to store and get JWT from cookies
  authjwt_token_location: set = {"cookies"}
  # Disable CSRF Protection for this example. default is True
  authjwt_cookie_csrf_protect: bool = False


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

