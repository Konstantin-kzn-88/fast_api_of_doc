# Первое приложение
# ________________________
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
# ________________________
# ________________________
# Параметризированный ответ
# ________________________
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id": item_id}
# ________________________
# ________________________
# Содержание в переменной пути
# ________________________
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}
# ________________________
# ________________________
# Преоопределенные значения пути
# ________________________
# from enum import Enum
#
# from fastapi import FastAPI
#
#
# class ModelName(str, Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"
#
#
# app = FastAPI()
#
#
# @app.get("/models/{model_name}")
# async def get_model(model_name: ModelName):
#     if model_name is ModelName.alexnet:
#         return {"model_name": model_name, "message": "Deep Learning FTW!"}
#
#     if model_name.value == "lenet":
#         return {"model_name": model_name, "message": "LeCNN all the images"}
#
#     return {"model_name": model_name, "message": "Have some residuals"}
# ________________________
# ________________________
# Query-параметры
# ________________________
# from fastapi import FastAPI
#
# app = FastAPI()
#
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
#
#
# @app.get("/items/")
# async def read_item(skip: int = 1, limit: int = 10):
#     return fake_items_db[skip : skip + limit]
# ________________________
# ________________________
# Query-параметры необязательные и булевы, а так смешение с path параметрами user_id и item_id
# ________________________
# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/users/{user_id}/items/{item_id}")
# async def read_user_item(
#     user_id: int, item_id: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {"description": "This is an amazing item that has a long description"}
#         )
#     return item
# ________________________
# ________________________
# Query-параметры и валидация строк + регулярки
# ________________________
# from typing import Annotated
# from fastapi import FastAPI, Query
#
# app = FastAPI()
#
#
# @app.get("/items/")
# async def read_items(
#     q: Annotated[
#         str | None,
#         Query(
#             alias="item-query",
#             title="Query string",
#             description="Query string for the items to search in the database that have a good match",
#             min_length=3,
#             max_length=50,
#             regex="^fixedquery$",
#             deprecated=True,
#         ),
#     ] = None
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
# ________________________
# ________________________
# Path-параметры и валидация числовых данных
# ________________________
# В этом примере при указании ge=1, параметр item_id должен быть больше или равен 1 ("greater than or equal").
# gt: больше (greater than)
# ge: больше или равно (greater than or equal)
# lt: меньше (less than)
# le: меньше или равно (less than or equal)
# from typing import Annotated
#
# from fastapi import FastAPI, Path
#
# app = FastAPI()
#
#
# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
# ):
#     results = {"item_id": item_id}
#     if q:
#         results.update({"q": q})
#     return results

# ________________________
# ________________________
# Body - Множество параметров
# ________________________
# from typing import Annotated
#
# from fastapi import Body, FastAPI
# from pydantic import BaseModel
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#
# class User(BaseModel):
#     username: str
#     full_name: str | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
# ):
#     results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#     return results

# ________________________
# ________________________
# Body - Поля
# ________________________
# from fastapi import Body, FastAPI
# from pydantic import BaseModel, Field
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length=300
#     )
#     price: float = Field(gt=0, description="The price must be greater than zero")
#     tax: float | None = None
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(embed=True)):
#     results = {"item_id": item_id, "item": item}
#     return results
# ________________________
# ________________________
# Body - Объявление примера
# ________________________
# Использование example и examples в OpenAPI¶
# При использовании любой из этих функций:
#
# Path()
# Query()
# Header()
# Cookie()
# Body()
# Form()
# File()
# вы также можете добавить аргумент, содержащий example или группу examples с дополнительной информацией, которая будет добавлена в OpenAPI.
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# app = FastAPI()
#
#
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None
#
#     class Config:
#         schema_extra = {
#             "example": {
#                 "name": "Foo",
#                 "description": "A very nice Item",
#                 "price": 35.4,
#                 "tax": 3.2,
#             }
#         }
#
#
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     results = {"item_id": item_id, "item": item}
#     return results

# ________________________
# ________________________
# Модель ответа тип возврата
# ________________________
# from fastapi import FastAPI
# from pydantic import BaseModel, EmailStr
#
# app = FastAPI()
#
#
# class UserBase(BaseModel):
#     username: str
#     email: EmailStr
#     full_name: str | None = None
#
#
# class UserIn(UserBase):
#     password: str
#
#
# class UserOut(UserBase):
#     pass
#
#
# class UserInDB(UserBase):
#     hashed_password: str
#
#
# def fake_password_hasher(raw_password: str):
#     return "supersecret" + raw_password
#
#
# def fake_save_user(user_in: UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
#     print("User saved! ..not really")
#     return user_in_db
#
#
# @app.post("/user/", response_model=UserOut)
# async def create_user(user_in: UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

# from src.model import spell_number

app = FastAPI()
templates = Jinja2Templates(directory="templates/")


@app.get('/')
def read_form():
    return 'hello world'


@app.get("/form")
def form_post(request: Request):
    result = [{'Введите': 'данные', '0': '0'}]
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@app.post("/form")
def form_post(request: Request, num: int = Form(...)):
    result = [{'A': num, 'B': num + 2}, {'C': num + 3, 'D': num + 4}]
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})
