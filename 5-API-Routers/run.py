from fastapi import FastAPI

from .database import engine
from . import models
from .routers import employee, user

app = FastAPI()

# Create the tables in the database
models.Base.metadata.create_all(engine)

app.include_router(employee.router)
app.include_router(user.router)