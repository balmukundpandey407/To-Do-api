from fastapi import FastAPI, APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, Userout, UserLogin, UserToken
from app.models.user import User, Base
from app.database import get_db, engine
from sqlalchemy.orm import Session
import uuid
from app.core.security import security, verify_password, hash_password, sign_jwt, decode_jwt

auth_router = APIRouter()

# Create all tables in the database
Base.metadata.create_all(bind=engine)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
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