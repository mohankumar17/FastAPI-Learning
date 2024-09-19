from fastapi import FastAPI, Response, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def db_connect():
    username = "postgres"
    password = "mohan"
    host = "localhost"
    port = "5432"
    database_name = "python_learning"    
    
    try:
        conn = psycopg2.connect(host=host, port=port, user=username, password=password, database=database_name, cursor_factory=RealDictCursor)
        return conn
    except Exception as ex:
        print(ex)

@app.get("/employees")
def fetch_employees(status: int | None = None):
    conn = db_connect()
    curr = conn.cursor()

    if status is None:
        curr.execute("SELECT * FROM employee;")
        employees = curr.fetchall()
        return employees
    
    is_active = "true" if status == 1 else "false"

    curr.execute(f"SELECT * FROM employee WHERE is_active={is_active};")
    active_employees = curr.fetchall()
    return active_employees

@app.get("/employees/{empID}")
def fetch_employee_id(empID: int, response: Response):
    conn = db_connect()
    curr = conn.cursor()

    curr.execute(f"SELECT * FROM employee WHERE emp_id={empID};")
    employee = curr.fetchall()
    
    if len(employee) == 0:
        response.status_code = 404
        return {
            "message": f"No employee found with ID: {empID}"
        }
    return employee[0]

@app.post("/employees")
def create_employee(response: Response, requestBody: dict = Body()):
    conn = db_connect()
    curr = conn.cursor()

    requestBody = (requestBody.get("emp_name"), requestBody.get("dob"), requestBody.get("department_id"), requestBody.get("emp_email"), requestBody.get("is_active"))

    curr.execute("INSERT INTO employee(emp_name, dob, department_id, emp_email, is_active) VALUES (%s, %s, %s, %s, %s) RETURNING emp_id", requestBody)
    conn.commit()

    emp_id = curr.fetchone().get("emp_id")

    response.status_code = 201
    return {
        "id": emp_id,
        "message": "New employee added"
    }

@app.put("/employees/{empID}")
def update_employe(empID: int, requestBody: dict = Body()):
    conn = db_connect()
    curr = conn.cursor()

    requestBody = (requestBody.get("emp_name"), requestBody.get("dob"), requestBody.get("department_id"), requestBody.get("emp_email"), requestBody.get("is_active"), empID)

    curr.execute("UPDATE employee SET emp_name = %s, dob = %s, department_id = %s, emp_email = %s, is_active= %s WHERE emp_id = %s", requestBody)
    conn.commit()

    if curr.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")

    return {
        "id": empID,
        "message": "Employee details updated"
    }


@app.delete("/employees/{empID}", status_code=204)
def delete_employe(empID: int):    
    conn = db_connect()
    curr = conn.cursor()

    curr.execute("DELETE FROM employee WHERE emp_id = %s", (empID,))
    conn.commit()

    if curr.rowcount == 0:
        raise HTTPException(status_code=404, detail=f"No employee found with ID: {empID}")
