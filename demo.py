from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

class Student(BaseModel):
    name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    year: int = Field(gt=0, lt=5)
    cgpa: float = Field(gt=0, lt=10)

@app.get("/")
def read(db: Session = Depends(get_db)):
    return db.query(models.Students).all()

@app.post("/")
def create(stu: Student, db: Session = Depends(get_db)):
    STU_model = models.Students(
        name=stu.name,
        department=stu.department,
        cgpa=stu.cgpa
    )
    db.add(STU_model)
    db.commit()
    db.refresh(STU_model)
    return STU_model

@app.put("/{id}")
def update(id: int, stu: Student, db: Session = Depends(get_db)):
    stu_model = db.query(models.Students).filter(models.Students.id == id).first()

    if stu_model is None:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist")

    stu_model.name = stu.name
    stu_model.department = stu.department
    stu_model.cgpa = stu.cgpa

    db.commit()
    return stu_model

@app.delete("/{id}")
def dele(id: int, db: Session = Depends(get_db)):
    stu_model = db.query(models.Students).filter(models.Students.id == id).first()
    
    if stu_model is None:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist")

    db.delete(stu_model)
    db.commit()
    return {"message": f"id {id} deleted"}
