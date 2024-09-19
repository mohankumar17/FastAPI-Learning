from typing import List
from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, ConfigDict, Field, ValidationError

app = FastAPI()

employees = [
     {
        "dob": "1990-04-15",
        "emp_email": "alice.johnson@example.com",
        "emp_name": "Alice Johnson",
        "department_id": 1,
        "emp_id": 1,
        "is_active": True
    }
]

class Employee(BaseModel):
    model_config = ConfigDict(extra='allow')
    
    emp_id: int = Field(default_factory=(lambda: len(employees) + 1))
    emp_name: str = Field(..., min_length=1, max_length=20)
    emp_email: str = Field(..., pattern="^.+@.+$")
    dob: str = Field(...)
    department_id: int = Field(...)
    is_active: bool = Field(default=False)

class EmployeeResponse(BaseModel):
    emp_id: int
    emp_name: str
    department_id: int
    is_active: bool

class EmployeePostResponse(BaseModel):
    emp_id: int
    emp_name: str
    class Config:
        orm_mode = True

@app.get("/employees", response_model=List[EmployeeResponse])
def fetch_employees():
    return employees

@app.post("/employees", status_code=201, response_model=EmployeePostResponse)
def create_employee(requestBody: Employee):
    employees.append(requestBody)

    return employees[-1]

@app.exception_handler(Exception)
def global_error_response(error, respone: Response):
    respone.status_code = 500
    return {
        "message": "Error occurred while processing",
        "error": error
    }