from typing import Optional

from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberExeption(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


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


class BookNoRaiting(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    autor: str = Field(min_length=1,
                       max_length=100)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=100)


BOOKS = []


@app.exception_handler(NegativeNumberExeption)
async def negativ_number_exception_handler(request: Request,
                                           exception: NegativeNumberExeption):
    return JSONResponse(
        status_code=418,
        content={'message': f'Why do you want {exception.books_to_return}'
                            f' books?'}
    )


@app.post('/books/login/')
async def book_login(book_id: int, username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == 'FastAPIUser' and password == 'test1234!':
        return BOOKS[book_id]
    return 'Invalid User'




@app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberExeption(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_book_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.get('/book/raiting/{book_id}', response_model=BookNoRaiting)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'ID {book_id} del'
    raise raise_item_cannot_be_found_exception()


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


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail='Book not found',
                         headers={'X-Headers-Error':
                                      'Nothing to be seen at the UUID'})