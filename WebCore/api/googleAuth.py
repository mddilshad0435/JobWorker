import os
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from starlette.responses import HTMLResponse
from starlette.responses import RedirectResponse
import uvicorn
from fastapi import  Request, APIRouter, Response
from authlib.integrations.starlette_client import OAuthError
from fastapi.responses import RedirectResponse
from WebCore.api.user import validUserEmail
from WebCore.auth.jwt_handler import encodeJWT
load_dotenv('.env')

authRouter = APIRouter()

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
REDIRECT_URL = os.environ.get('REDIRECT_URL')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)


@authRouter.route('/auth')
async def googleAuth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url="/user/login/")
    user_data = access_token.get('userinfo')
    if user_data:
        user = validUserEmail(user_data['email'],user_data['name'])
        if user:
            url = {1:"/user/superuser/",2:"/user/worker/",3:"/user/customer/"}
            access_token = encodeJWT(user_data['email'])
            redirect_url = user['user_type']
            response  = RedirectResponse(url=url[redirect_url])
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
            return response
        else:
            access_token = encodeJWT(user_data['email'])
            response  = RedirectResponse(url="/user/customer/")
            response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
            return response
    return RedirectResponse(url="/user/login/")


@authRouter.route("/login/google/")
async def GoogleLogin(request: Request):
    redirect_url = REDIRECT_URL
    try:
        return await oauth.google.authorize_redirect(request,redirect_url)
    except:
        return RedirectResponse(url="/user/login/")

# # OAuth settings
# GOOGLE_CLIENT_ID1 = os.environ.get('GOOGLE_CLIENT_ID1')
# GOOGLE_CLIENT_SECRET1 = os.environ.get('GOOGLE_CLIENT_SECRET1')

# # Set up oauth
# config_data1 = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID1, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET1}
# starlette_config1 = Config(environ=config_data1)
# oauth1 = OAuth(starlette_config1)
# oauth1.register(
#     name='google',
#     server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#     client_kwargs={'scope': 'openid email profile'},
# )

# @authRouter.route("/signup/google/")
# async def Googlesignup(request: Request):
#     redirect_url = "http://127.0.0.1:8000/authSignup"
#     print("Come here")
#     return await oauth1.google.authorize_redirect(request,redirect_url)


# @authRouter.route('/authSignup')
# async def googleAuth2(request: Request):
#     try:
#         access_token = await oauth1.google.authorize_access_token(request)
#     except OAuthError:
#         return RedirectResponse(url="/home")
#     print(access_token)
#     user_data = access_token.get('userinfo')
#     print(user_data)
#     user = validUsersignup(user_data['email'],user_data['name'])
#     print(user)
#     if user:
#         print("User is valid")
#         access_token = encodeJWT(user_data['email'])
#         response  = RedirectResponse(url="/user/customer/")
#         response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
#         return response
#     else:
#         print("User is already register")
#         return RedirectResponse(url="/user/login/")