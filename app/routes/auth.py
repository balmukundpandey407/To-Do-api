from fastapi import FastAPI, APIRouter, Depends,Header, HTTPException
from schemas.user import UserCreate, Userout, Userupdate, UserLogin, UserToken
from models.user import User, Base
from bcrypt import checkpw, hashpw, gensalt
import jwt
from decouple import config
import time
from database import get_db, engine
from sqlalchemy.orm import Session
from typing import Optional, Annotated
import uuid


JWT_SECRET_KEY = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")

auth_router = APIRouter()

Auth_prefix = 'Bearer '

# Create all tables in the database
Base.metadata.create_all(bind=engine)


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

def get_current_user(
    db: Session = Depends(get_db),
    authorization: Annotated[Optional[str], Header()] = None
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is missing"
        )

    if not authorization.startswith(Auth_prefix):
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    token = authorization[len(Auth_prefix):]

    decoded_token = decode_jwt(token)

    if not decoded_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == decoded_token["user_id"]
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return Userout(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )


@auth_router.post("/register")
def sign_up_user(sign_up_data: UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existing_user = db.query(User).filter(User.email == sign_up_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists please login instead")

    # Hash the password
    hashed_password = hash_password(sign_up_data.password)
    
    new_user = User(
     id= str(uuid.uuid4()),
     first_name=sign_up_data.first_name,
     last_name=sign_up_data.last_name,
     email=sign_up_data.email,
     password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@auth_router.post("/login",response_model=UserToken)
def login_user(login_data: UserLogin, db: Session = Depends(get_db), ):
    # Find the user by email
    user = db.query(User).filter(User.email == login_data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Verify the password
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    # Generate a JWT token
    token = sign_jwt(user.id)
    if not token:
        raise HTTPException(status_code=500, detail="Token generation failed")
    return UserToken(token=token)