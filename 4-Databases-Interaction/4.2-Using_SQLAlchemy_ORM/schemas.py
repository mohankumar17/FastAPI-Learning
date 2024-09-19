from pydantic import BaseModel, ConfigDict, Field
from datetime import date

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