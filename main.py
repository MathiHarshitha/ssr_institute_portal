from fastapi import FastAPI

from database import engine, Base
from models.student import Student
from routers.student import router as student_router
from models.user import User
from routers.user import router as user_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SSR Institute ERP"
    }
