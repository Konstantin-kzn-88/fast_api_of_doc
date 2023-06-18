from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    'book_6': {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
}


@app.get('/')
async def read_all_books(skip_book: str | None = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS


@app.get('/{book_name}')
async def read_books(book_name: str):
    return BOOKS[book_name]


@app.post('/')
async def create_books(book_title: str, book_author: str):
    current_book_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']


@app.put('/{book_name}')
async def update_books(book_name: str, book_title: str, book_author: str):
    book_info = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_info
    return book_info

@app.delete('/{book_name}')
async def delete_books(book_name: str):
    del BOOKS[book_name]
    return f'Book {book_name} delete'

# ___________Assigment_____________
@app.get('/assigment/')
async def read_book_assigment(book_name:str):
    return BOOKS[book_name]

@app.delete('/assigment/')
async def delete_books_assigment(book_name: str):
    del BOOKS[book_name]
    return f'Book {book_name} delete'
