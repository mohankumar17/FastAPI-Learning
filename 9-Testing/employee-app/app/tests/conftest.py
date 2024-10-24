from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
from app.run import app
from app import models, oauth2

from fastapi.testclient import TestClient
import pytest
from app.schemas import UserResponse

host = settings.DB_HOST
port = settings.DB_PORT
username = settings.DB_USERNAME
password = settings.DB_PASSWORD
database_name = settings.DB_DATABASE_NAME + "_test"

# Create an engine connected to the Postgres test database
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
TestingSession = sessionmaker(bind=engine)

#@pytest.fixture(scope="module")
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()

#@pytest.fixture(scope="module")
@pytest.fixture(scope="function")
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    reqBody = {
        "user_email": "paul@test.com",
        "user_password": "paul@123"
    }
    res = client.post("/users/", json = reqBody)
    assert res.status_code == 201
    
    user = res.json()
    user["user_password"] = reqBody["user_password"]
    return user

@pytest.fixture()
def test_user_2(client):
    reqBody = {
        "user_email": "tina@test.com",
        "user_password": "tina@456"
    }
    res = client.post("/users/", json = reqBody)
    assert res.status_code == 201
    
    user = res.json()
    user["user_password"] = reqBody["user_password"]
    return user

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user['user_id']})

@pytest.fixture
def token_2(test_user_2):
    return oauth2.create_access_token({"user_id": test_user_2['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def authorized_client_2(client, token_2):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_2}"
    }

    return client

@pytest.fixture()
def add_departments(session):
    departments = [
        {
            "dept_name": "Sales" 
        },
        {
            "dept_name": "Marketing" 
        },
        {
            "dept_name": "HR" 
        },
        {
            "dept_name": "IT" 
        }
    ]

    new_departments = list(map(lambda dept: models.Department(dept_name = dept.get("dept_name")), departments))
    session.add_all(new_departments)
    session.commit()

    departments = session.query(models.Department).all()

    return departments

@pytest.fixture()
def add_employees(session, test_user, test_user_2):
    employees = [
        {
            "emp_name": "John Doe",
            "dob": "1985-04-15",
            "department_id": 1,
            "emp_email": "john.doe@example.com",
            "is_active": False,
            "user_id": test_user["user_id"]
        },
        {
            "emp_name": "Alex Wright",
            "dob": "1998-11-21",
            "department_id": 3,
            "emp_email": "alex.wright@example.com",
            "is_active": True,
            "user_id": test_user["user_id"]
        },
        {
            "emp_name": "Roger Fed",
            "dob": "1996-02-08",
            "department_id": 2,
            "emp_email": "roger.fed@example.com",
            "is_active": True,
            "user_id": test_user_2["user_id"]
        }
    ]

    new_emps = list(map(lambda emp: models.Employee(**emp), employees))
    session.add_all(new_emps)
    session.commit()

    employees = session.query(models.Employee).all()

    return employees