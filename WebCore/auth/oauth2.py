from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,Depends,status, Request
from . import jwt_handler
# from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(request: Request):
    data = request.cookies.get("access_token")
    try:
        data = data.split()[1]
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return jwt_handler.validUser(data,credentials_exception)
    except:
        return None