# this file is responsible for signing , encoding , decoding and returning jwts

import time
import jwt
from decouple import config
import os
import sys
from dotenv import load_dotenv
from WebCore.schemas.request.user import TokenData
from typing import Optional


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, '.env'))
sys.path.append(BASE_DIR)


JWT_SECRET = os.environ['secret']
JWT_ALGORITHM = os.environ['algorithm']


def token_response(token: str):
    return {
        "access token": token
    }


def encodeJWT(userID: str):
    payload = {
        "userID": userID,
        "expiry": time.time() + 20000
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decode_token
    except:
        return None

def validUser(token: str,credentials_exception: Optional[str] = None):
    try:
        payload = decodeJWT(token)
        email: str = payload.get("userID")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except:
        return None
