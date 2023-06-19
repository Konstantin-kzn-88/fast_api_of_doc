from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    autor: str = Field(min_length=1,
                       max_length=100)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=100)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            'example': {
                'id': 'b1a3f09a-ff2f-491e-a980-27ea60925751',
                'title': 'Comp prog',
                'autor': 'Kuznetsov',
                'description': 'Good book',
                'rating': 100
            }
        }


BOOKS = []


@app.get('/')
async def read_all_books():
    if len(BOOKS)<1:
        create_book_no_api()
    return BOOKS


@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book


def create_book_no_api():
    book_1 = Book(id='1dbd6004-3854-496e-8572-c1a908e1c443',
                  title="Comp book_1",
                  autor='autor_1',
                  description='description_1',
                  rating=50)

    book_2 = Book(id='7f94c7fb-55eb-46aa-be23-cc4e1ad83019',
                  title="Comp book_2",
                  autor='autor_2',
                  description='description_2',
                  rating=70)

    book_3 = Book(id='a1a3f09a-ff2f-491e-a980-27ea60925751',
                  title="Comp book_3",
                  autor='autor_3',
                  description='description_3',
                  rating=80)

    book_4 = Book(id='23a27fa4-eee7-4b01-8b72-660d73512336',
                  title="Comp book_4",
                  autor='autor_4',
                  description='description_4',
                  rating=90)

    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)