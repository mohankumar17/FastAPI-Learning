from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

# Define a model
class Employee(Base):
    __tablename__ = 'employee'
    emp_id = Column(Integer, primary_key=True)
    emp_name = Column(String(50), nullable=False)
    dob = Column(Date)
    department_id = Column(Integer, server_default="1", nullable=False)
    emp_email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, server_default="TRUE")


