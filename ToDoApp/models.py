from sqlalchemy import Boolean, ForeignKey, Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    hahed_password = Column(String)
    is_active = Column(Boolean, default=True)

    todos = relationship('Todos', back_populates='owner')



class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(String)
    complete = Column(Boolean, default=False)
    owner_id= Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', back_populates='todos')