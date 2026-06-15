from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.student import Student
from models.student import Student as StudentModel

router = APIRouter()


@router.post("/students")
def create_student(student: Student, db: Session = Depends(get_db)):
    new_student = StudentModel(
        name=student.name,
        email=student.email,
        phone=student.phone
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student Created",
        "student": {
            "id": new_student.id,
            "name": new_student.name,
            "email": new_student.email,
            "phone": new_student.phone
        }
    }


@router.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(StudentModel).all()

    return students

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student:
        return {"message": "Student not found"}

    return student    

@router.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: Student,
    db: Session = Depends(get_db)
):
    existing_student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not existing_student:
        return {"message": "Student not found"}

    existing_student.name = student.name
    existing_student.email = student.email
    existing_student.phone = student.phone

    db.commit()
    db.refresh(existing_student)

    return {
        "message": "Student Updated",
        "student": existing_student
    }    

@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(StudentModel).filter(
        StudentModel.id == student_id
    ).first()

    if not student:
        return {"message": "Student not found"}

    db.delete(student)
    db.commit()

    return {
        "message": "Student Deleted"
    }    
