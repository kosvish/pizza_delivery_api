from fastapi import APIRouter, status, Depends
from database import Session, engine
from schemas import SingUpModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from schemas import LoginModel
from fastapi.encoders import jsonable_encoder
import jwt
from config import SECRET
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=SECRET)

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = jwt.decode(token, key=SECRET)
    db_user = session.query(User).filter(user["username"] == User.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@auth_route.get("/")
async def hell():
    return {"message": "Hello World"}


@auth_route.post("/signup", status_code=status.HTTP_201_CREATED, response_model=SingUpModel)
async def signup(user: SingUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    session.add(new_user)
    session.commit()

    return new_user


# login routes

@auth_route.post("/login")
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        payload = {
            "username": db_user.username,
            "email": db_user.email,
            "sub": db_user.id
        }
        access_token = jwt.encode(payload=payload, key=SECRET, algorithm='HS256')
        response = {
            "access": access_token,
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")



