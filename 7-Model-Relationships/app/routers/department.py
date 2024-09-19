from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..database import get_db
from .. import models

router = APIRouter(
    prefix="/departments",
    tags=['Department']
)

@router.get("/")
def fetch_departments(db: Session = Depends(get_db)):
    depts = db.query(models.Department).all()
    return depts

@router.get("/active")
def fetch_department_employees(db: Session = Depends(get_db)):
    active_departments = db.query(models.Department).join(target=models.Employee, onclause=models.Department.dept_id == models.Employee.department_id).all()

    return active_departments
