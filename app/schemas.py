from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum


# ------------------------------
# ENUM FOR CALCULATION TYPES
# ------------------------------
class CalculationType(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"


# ------------------------------
# USER SCHEMAS
# ------------------------------
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


# ------------------------------
# CALCULATION SCHEMAS
# ------------------------------
class CalculationBase(BaseModel):
    a: float
    b: float
    type: CalculationType


class CalculationCreate(CalculationBase):
    """
    Frontend provides only a, b, type.
    user_id is extracted from JWT, not passed in request body.
    """
    pass


class CalculationUpdate(BaseModel):
    """
    PUT update request.
    All are optional because user may update only one field.
    """
    a: Optional[float] = None
    b: Optional[float] = None
    type: Optional[CalculationType] = None


from pydantic import BaseModel
from typing import Literal

class CalculationType(str, Enum):
    add = "add"
    subtract = "subtract"
    multiply = "multiply"
    divide = "divide"

class CalculationCreate(BaseModel):
    a: float
    b: float
    type: CalculationType

class CalculationRead(BaseModel):
    a: float
    b: float
    type: str
    result: float

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            a=obj.a,
            b=obj.b,
            type=obj.type.lower(),
            result=obj.result
        )


from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # formerly orm_mode

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str