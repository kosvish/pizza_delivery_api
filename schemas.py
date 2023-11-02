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
