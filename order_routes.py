from typing import Annotated

from fastapi import APIRouter, HTTPException
from auth_routes import oauth2_scheme
from fastapi import Depends
from fastapi import status
from models import User, Order
from schemas import OrderModel
from jwt import decode
from config import SECRET
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

session = Session(bind=engine)


@order_route.get("/")
async def hell(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = decode(token, key=SECRET, algorithms="HS256")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "Hello Order"}


@order_route.post("/order")
async def place_an_order(order: OrderModel, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        current_user = decode(token, key=SECRET, algorithms="HS256")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    user = session.query(User).filter(User.username == current_user["username"]).first()

    new_order = Order(
        pizza_sizes=order.pizza_sizes,
        quantity=order.quantity,
        user_id=current_user["sub"],
    )
    new_order.user = user
    session.add(new_order)
    session.commit()

    response = {
        "pizza_sizes": new_order.pizza_sizes,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)
