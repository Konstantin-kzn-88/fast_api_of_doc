from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine



class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    lastname: str
    password: str


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password: object) -> object:
    return bcrypt_context.hash(password)

@app.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.firstname = create_user.first_name
    create_user_model.lastname = create_user.lastname
    
    hash_password = get_password_hash(create_user.password)
    
    create_user_model.hahed_password = hash_password
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()
    return successful_response(201)

def successful_response(status_code:int):
    return {
        'status': status_code,
        'transaction': 'successful'
    }

