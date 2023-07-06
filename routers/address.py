import sys
sys.path.append('..')


from  fastapi import Depends, APIRouter, HTTPException
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user

router = APIRouter(
    prefix='/address',
    tags=['address'],
    responses={404:{'Description':'Not found'}}

)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Address(BaseModel):
    address1: str
    address2: str
    city: str
    state: str
    country: str
    postalcode: str


@router.post('/')
async def create_address(address: Address,
                         user: dict = Depends(get_current_user),
                         db: Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail='Not Found')
    address_model = models.Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('user_id')).first()
    user_model.address_id = address_model.id
    db.add(user_model)
    db.commit()





