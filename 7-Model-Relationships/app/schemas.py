from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import date, datetime

class Employee(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    emp_name: str = Field(..., min_length=1, max_length=20)
    emp_email: str = Field(..., pattern="^.+@.+$")
    dob: date = Field(...)
    department_id: int = Field(...)
    is_active: bool = Field(default=False)

class EmployeeRequest(Employee):
    pass

class EmployeeResponse(Employee):
    emp_id: int = Field(...)
    user_id: int

class UserRequest(BaseModel):
    user_email: EmailStr = Field(...)
    user_password: str = Field(..., min_length=5)

class UserResponse(BaseModel):
    user_id: int
    user_email: EmailStr
    updated_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    