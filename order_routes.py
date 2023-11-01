from fastapi import APIRouter

order_route = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@order_route.get("/order")
async def hell():
    return {"message": "Hello Order"}
