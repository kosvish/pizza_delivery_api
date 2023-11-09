from pydantic import BaseModel
from typing import Optional


class SingUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_stuff": False,
                "is_active": True,
                "id": 0
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_sizes: Optional[str] = "SMALL"
    user_id: Optional[int]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "quantity": 2,
                "pizza_sizes": "LARGE",
                "user_id": 0,
                "id": 0
            }
        }
