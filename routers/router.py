from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import sessionlocal
from pydantic import BaseModel, Field
from models.models import Students

router = APIRouter()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schema (Moved here)
class Student(BaseModel):
    name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    year: int = Field(gt=0, lt=5)
    cgpa: float = Field(gt=0, lt=10)

@router.get("/")
def read_students(db: Session = Depends(get_db)):
    return db.query(Students).all()

@router.post("/")
def create_student(stu: Student, db: Session = Depends(get_db)):
    new_student = Students(
        name=stu.name,
        department=stu.department,
        year=stu.year,
        cgpa=stu.cgpa
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.put("/{id}")
def update_student(id: int, stu: Student, db: Session = Depends(get_db)):
    stu_model = db.query(Students).filter(Students.id == id).first()
    if not stu_model:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist")
    
    stu_model.name = stu.name
    stu_model.department = stu.department
    stu_model.year = stu.year
    stu_model.cgpa = stu.cgpa

    db.commit()
    return stu_model

@router.delete("/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    stu_model = db.query(Students).filter(Students.id == id).first()
    if not stu_model:
        raise HTTPException(status_code=404, detail=f"ID {id} does not exist")

    db.delete(stu_model)
    db.commit()
    return {"message": f"id {id} deleted"}
