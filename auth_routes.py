from fastapi import APIRouter, status
from database import Session, engine
from schemas import SingUpModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)


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


