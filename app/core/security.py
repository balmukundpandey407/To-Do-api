from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bcrypt import checkpw, hashpw, gensalt
import time
import jwt
import os

security = HTTPBearer()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    
    if checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True
    return False

def hash_password(password: str) -> str:
    return hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

def sign_jwt(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": time.time() + 900  # Token expires in 15 minutes
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
