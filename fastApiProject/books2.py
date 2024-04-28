from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


# real books objects

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


# validations
class BookRequest(BaseModel):
    id: Optional[int] = None  # either integer or None or null
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


Books = [
    Book(1, 'Korbo ki?', 'Rifat Zaman', 'Good One', 6),
    Book(2, 'Kortesi ki?', 'Rayhan', 'GG', 4),
    Book(3, 'HMMMM', 'Asif', 'Shera', 7),
    Book(4, 'Janina', 'Kabir', 'Shera vai shera', 8),
    Book(5, 'Chyh', 'Zishan_Vai', 'Shera 2', 5),
    Book(6, 'Nosto', 'Fahim_Vai', 'Shera vai shera 2', 8),
]


@app.get("/books")
async def read_all_books():
    return Books


# without validation
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())
    # Books.append(new_book)
    Books.append(find_book_id(new_book))  # for indexing


def find_book_id(book: Book):
    # if len(Books) > 0:
    #     book.id = Books[-1].id + 1
    # else:
    #     book.id = 1

    book.id = 1 if len(Books) == 0 else Books[-1].id + 1  # using ternary operator

    return book
