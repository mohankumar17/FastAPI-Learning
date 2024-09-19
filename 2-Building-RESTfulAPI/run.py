from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body

app = FastAPI()

employees = [
    {
        "id": 1,
        "name": "Paul",
        "department": "HR",
        "isActive": True,
        "salary": 100000
    }
]

def find_employee(empID):
    employee = list(filter(lambda emp: emp.get("id") == empID, employees))
    return employee

@app.get("/employees")
def fetch_employees(status: int | None = None):
    if status is None:
        return employees
    
    print(status)
    active_employees = list(filter(lambda emp: emp.get("isActive") == status, employees))
    return active_employees

@app.get("/employees/{empID}")
def fetch_employee_id(empID: int, response: Response):
    employee = find_employee(empID)
    if len(employee) == 0:
        response.status_code = 404
        return {
            "message": f"No employee found with ID: {empID}"
        }
    return employee[0]

@app.post("/employees")
def create_employee(response: Response, requestBody: dict = Body()):
    requestBody["id"] = len(employees) + 1
    employees.append(requestBody)

    response.status_code = 201
    return {
        "id": len(employees),
        "message": "New employee added"
    }

@app.put("/employees/{empID}")
def update_employe(empID: int, requestBody: dict = Body()):
    employee = find_employee(empID)
    if len(employee) == 0:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")

    requestBody["id"] = empID
    employees.pop(empID-1)
    employees.insert(empID-1, requestBody)

    return {
        "id": empID,
        "message": "Employee details updated"
    }

@app.delete("/employees/{empID}", status_code=204)
def delete_employe(empID: int):
    employee = find_employee(empID)
    if len(employee) == 0:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")

    employees.pop(empID-1)

    '''return {
        "id": empID,
        "message": "Employee details deleted"
    }'''