from fastapi import HTTPException
from app.config import settings
import pytest

def test_add_employee(authorized_client, add_departments):
    req = {
        "emp_name": "John Doe",
        "dob": "1985-04-15",
        "department_id": 1,
        "emp_email": "john.doe@example.com",
        "is_active": False
    }
    res = authorized_client.post("/employees", json=req)
    emp_res = res.json()

    assert res.status_code == 201
    assert emp_res.get("message") == "New employee added"
    
    emp = emp_res.get("data")
    assert emp.get("emp_name") == req.get("emp_name")
    assert emp.get("dob") == req.get("dob")
    assert emp.get("department_id") == req.get("department_id")
    assert emp.get("emp_email") == req.get("emp_email")
    assert emp.get("is_active") == req.get("is_active")

def test_fetch_employees(authorized_client, add_departments, add_employees):
    res = authorized_client.get("/employees")
    
    assert len(res.json()) == 2
    assert res.status_code == 200

def test_fetch_active_employees(authorized_client, add_departments, add_employees):
    res = authorized_client.get(f"/employees?status={1}")
    
    assert res.json()[0].get("emp_email") == add_employees[1].emp_email
    assert res.status_code == 200

def test_user_2_fetch_employees(authorized_client_2, add_departments, add_employees):
    res = authorized_client_2.get("/employees")
    
    assert len(res.json()) == 1
    assert res.status_code == 200

def test_unauthorized_fetch_employees(client, add_departments, add_employees):
    res = client.get("/employees")
    assert res.status_code == 401

def test_fetch_one_employee(authorized_client, add_departments, add_employees):
    res = authorized_client.get(f"/employees/{add_employees[0].emp_id}")
    
    assert res.json().get("emp_name") == add_employees[0].emp_name
    assert res.status_code == 200

def test_fetch_non_existing_employee(authorized_client, add_departments, add_employees):
    res = authorized_client.get(f"/employees/{99}")
    
    assert res.status_code == 404

def test_update_employee(authorized_client, add_departments, add_employees):
    req = {
        "emp_name": "John Doe",
        "dob": "1975-04-15",
        "department_id": 1,
        "emp_email": "john.doe@gmail.com",
        "is_active": False
    }
    res = authorized_client.put(f"/employees/{add_employees[0].emp_id}", json=req)

    assert res.status_code == 200
    assert res.json().get("total_records_updated") == 1

def test_update_other_user_employee(authorized_client_2, add_departments, add_employees):
    req = {
        "emp_name": "John Doe",
        "dob": "1975-04-15",
        "department_id": 1,
        "emp_email": "john.doe@gmail.com",
        "is_active": False
    }
    res = authorized_client_2.put(f"/employees/{add_employees[0].emp_id}", json=req)

    assert res.status_code == 404

def test_delete_non_exists_employee(authorized_client, add_departments, add_employees):
    res = authorized_client.delete(f"/employees/{99}")

    assert res.status_code == 404

def test_delete_employee(authorized_client, add_departments, add_employees):
    res = authorized_client.delete(f"/employees/{add_employees[0].emp_id}")

    assert res.status_code == 204