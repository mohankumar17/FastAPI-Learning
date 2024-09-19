from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Hello, Welcome to FastAPI Framweork"
    }

@app.get("/posts", status_code=200)
def fetch_posts():
    return {
        "posts": [
            {
                "id": 101,
                "message": "Hi all. Good Morning."
            },
            {
                "id": 102,
                "message": "Having a great day in Paris."
            }
        ]
    }

@app.post("/posts", status_code=201)
def add_posts(request: dict = Body()):
    print(request)
    return {
        "id": 1,
        "message": "Post added"
    }
