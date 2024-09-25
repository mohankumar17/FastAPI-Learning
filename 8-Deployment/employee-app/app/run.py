from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import time

#from .database import engine
#from . import models
from .routers import employee, user, auth, department

app = FastAPI()

# Allow API to be accessed from below domains
'''origins = [
    "http://localhost",
    "http://localhost:8000",
]'''

# Allow API to be accessed from every domain
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the tables in the database. But, we will be using alembic to create tables
#models.Base.metadata.create_all(engine)

app.include_router(employee.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(department.router)

@app.get("/")
def health_check():
    return {
        "status": "App is up and running!!"
    }

def error_response(errorDetails):
    error_response =  {
        "message": errorDetails.get("message"),
        "description": errorDetails.get("description"),
        "dateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    }
    return error_response

@app.exception_handler(Exception)
def global_error_handler(request, error):
    errorDetails = {
        "message": "Server error",
        "description": str(error)
    }

    return JSONResponse(status_code=500, content=error_response(errorDetails))
