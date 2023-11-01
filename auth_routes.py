from fastapi import APIRouter

auth_route = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_route.get("/")
async def hell():
    return {"message": "Hello World"}
