from fastapi import FastAPI
from models import models
from database import engine
from routers import router

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(router.router, prefix="/students", tags=["Students"])

@app.get("/")
def root():
    return {"message": "Welcome to the Student API"}
