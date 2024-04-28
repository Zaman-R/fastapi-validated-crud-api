from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


# real books objects

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# validations
class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id is not needed')  # either integer or None or null
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gte=1900, lte=2100)

    class Config:
        schema_extra = {
            'example': {
                'title': 'A new book',
                'author': 'rifat vai',
                'description': 'gg ezy',
                'rating': 5,
                'published_date': 1998
            }
        }


Books = [
    Book(1, 'Korbo ki?', 'Rifat Zaman', 'Good One', 6, 1993),
    Book(2, 'Kortesi ki?', 'Rayhan', 'GG', 4, 2001),
    Book(3, 'HMMMM', 'Asif', 'Shera', 7, 2005),
    Book(4, 'Janina', 'Kabir', 'Shera vai shera', 8, 2004),
    Book(5, 'Chyh', 'Zishan_Vai', 'Shera 2', 5, 1998),
    Book(6, 'Nosto', 'Fahim_Vai', 'Shera vai shera 2', 8, 2024),
]


@app.get("/books")
async def read_all_books():
    return Books


@app.get("/books/{id}")  # path parameter for single one
async def read_book(book_id: int = Path(gt=0)):  # need to be 0 or through errors
    for book in Books:
        if book.id == book_id:
            return book


@app.get("/books/")  # query parameter for a set of something
async def read_book_rating(rating: int = Query(gt=0, lt=6)):
    books_by_rating = []
    for book in Books:
        if book.rating == rating:
            books_by_rating.append(book)

    return books_by_rating


@app.get("/books/publish/")
async def read_books_by_date(publish_date: int = Query(gt=1996, lt=2100)):
    books_to_return = []
    for book in Books:
        if book.published_date == publish_date:
            books_to_return.append(book)
    return books_to_return


# without validation
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    # Books.append(new_book)
    Books.append(find_book_id(new_book))  # for indexing


@app.put("/books/update_book")
async def update_book(book_request: BookRequest):
    for book in Books:
        if book.id == book_request.id:
            book.title = book_request.title
            book.rating = book_request.rating


@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for book in Books:
        if book.id == book_id:
            Books.remove(book)


def find_book_id(book: Book):
    # if len(Books) > 0:
    #     book.id = Books[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(Books) == 0 else Books[-1].id + 1  # using ternary operator

    return book
