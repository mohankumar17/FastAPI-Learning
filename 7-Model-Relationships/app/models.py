from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Define a model
class Employee(Base):
    __tablename__ = 'employees'
    emp_id = Column(Integer, primary_key=True)
    emp_name = Column(String(50), nullable=False)
    dob = Column(Date)
    department_id = Column(Integer, ForeignKey(name="emp_dept_fk", column="departments.dept_id", ondelete="CASCADE"), nullable=True)
    emp_email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, server_default="FALSE")
    user_id = Column(Integer, ForeignKey(name="emp_user_fk", column="users.user_id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")
    department = relationship("Department")

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(String, nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Department(Base):
    __tablename__ = 'departments'
    dept_id = Column(Integer, primary_key=True)
    dept_name = Column(String, nullable=False, unique=True)