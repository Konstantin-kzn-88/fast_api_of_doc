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
from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item