from fastapi import APIRouter
from auth_routes import get_current_user
from fastapi import Depends
from models import User
order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@order_route.get("/order")
async def hell(data: User = Depends(get_current_user)):
    return {"message": "Hello Order"}
