from fastapi import FastAPI
from cherrypick_ai.config import DB_USERNAME

app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "${DB}"}