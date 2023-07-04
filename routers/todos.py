import sys

sys.path.append('..')

from starlette import status
from starlette.responses import RedirectResponse

from typing import Optional
from fastapi import Form, Request, Depends, HTTPException, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from .auth import get_current_user, get_user_exception

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {'description': 'Not found'}}

)

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates/')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/', response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todos).filter(models.Todos.owner_id == 1).all()
    return templates.TemplateResponse('home.html', {'request': request, 'todos': todos})


@router.get('/add-todo', response_class=HTMLResponse)
async def add_new_todo(request: Request):
    return templates.TemplateResponse('add_todo.html', {'request': request})


@router.post('/add-todo', response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...),
                      description: str = Form(...),
                      priority: str = Form(...),
                      db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = 1

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)



@router.get('/edit-todo/{todo_id}', response_class=HTMLResponse)
async def edit_todo(request: Request):
    return templates.TemplateResponse('edit_todo.html', {'request': request})

# API без HTML
# class ToDo(BaseModel):
#     title: str
#     description: Optional[str]
#     priority: int = Field(gt=0, lt=6, description='Must be between 1-5')
#     complete: bool
#
# @router.get('/test')
# async def test(request: Request):
#     return templates.TemplateResponse('register.html', {'request': request})
#
#
# @router.get('/test')
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Todos).all()
#
# @router.get('/user')
# async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     return db.query(models.Todos).filter(models.Todos.owner_id == user.get('user_id')).all()
#
#
# @router.get('/{todo_id}')
# async def read_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model = db.query(models.Todos). \
#         filter(models.Todos.id == todo_id). \
#         filter(models.Todos.owner_id == user.get('user_id')) \
#         .first()
#     if todo_model is not None:
#         return todo_model
#     raise http_exception()
#
#
# @router.post('/')
# async def create_todo(todo: ToDo, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model = models.Todos()
#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.priority = todo.priority
#     todo_model.complete = todo.complete
#     todo_model.owner_id = user.get('user_id')
#
#     db.add(todo_model)
#     db.commit()
#
#     return successful_response(201)
#
#
# @router.put('/{todo_id}')
# async def update_todo(todo_id: int, todo: ToDo, user: dict = Depends(get_current_user),  db: Session = Depends(get_db)):
#
#     if user is None:
#         raise get_user_exception()
#
#     todo_model = db.query(models.Todos).\
#         filter(models.Todos.id == todo_id).\
#         filter(models.Todos.owner_id == user.get('user_id'))\
#         .first()
#     if todo_model is None:
#         raise http_exception()
#     todo_model.title = todo.title
#     todo_model.description = todo.description
#     todo_model.priority = todo.priority
#     todo_model.complete = todo.complete
#
#     db.add(todo_model)
#     db.commit()
#
#     return successful_response(200)
#
#
# @router.delete('/{todo_id}')
# async def delete_todo(todo_id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()
#     todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
#     if todo_model is None:
#         raise http_exception()
#     db.query(models.Todos).filter(models.Todos.id == todo_id).\
#         filter(models.Todos.owner_id == user.get('user_id')).\
#         delete()
#     db.commit()
#
#     return successful_response(200)
#
#
# def http_exception():
#     return HTTPException(status_code=404, detail="Todo not found")
#
#
# def successful_response(status_code: int):
#     return {
#         'status': status_code,
#         'transaction': 'successful'
#     }
