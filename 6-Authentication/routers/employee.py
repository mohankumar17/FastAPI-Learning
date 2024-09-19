from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix="/employees",
    tags=['Employees']
)

@router.get("/", response_model=List[schemas.EmployeeResponse])
def fetch_employees(status: bool | None = None, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    if status is None:
        employees = db.query(models.Employee).all()
        return employees

    employees = db.query(models.Employee).filter(models.Employee.is_active == status).all()
    return employees

@router.get("/{empID}", response_model=schemas.EmployeeResponse)
def fetch_employee_id(empID: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    employee = db.query(models.Employee).filter(models.Employee.emp_id == empID).all()
    
    if len(employee) == 0:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")
    
    return employee[0]

@router.post("/", status_code=201)
def create_employee(requestBody: schemas.EmployeeRequest, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):

    #print(user_id)
    new_employee = models.Employee(**requestBody.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    
    return {
        "id": new_employee.emp_id,
        "data": new_employee,
        "message": "New employee added"
    }

@router.put("/{empID}")
def update_employe(empID: int, requestBody: schemas.EmployeeRequest, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Employee).filter(models.Employee.emp_id == empID)
    employee = query.first()
    
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")
    
    out = query.update(requestBody.model_dump(), synchronize_session=False)
    db.commit()

    return {
        "id": empID,
        "total_records_updated": out,
        "message": "Employee details updated"
    }


@router.delete("/{empID}", status_code=204)
def delete_employe(empID: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):    
    query = db.query(models.Employee).filter(models.Employee.emp_id == empID)
    employee = query.first()
    
    if employee is None:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")
    
    query.delete(synchronize_session=False)
    db.commit()