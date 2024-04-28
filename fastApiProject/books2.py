from fastapi import FastAPI, Body

app = FastAPI()

# real books objects

class Book:
    id : int
    title : str
    author: str
    description : str
    rating : int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


Books =[
    Book(1,'Korbo ki?', 'Rifat Zaman', 'Good One', 6),
    Book(2,'Kortesi ki?', 'Rayhan', 'GG', 4),
    Book(3,'HMMMM', 'Asif', 'Shera', 7),
    Book(4,'Janina', 'Kabir', 'Shera vai shera', 8),
    Book(5,'Chyh', 'Zishan_Vai', 'Shera 2', 5),
    Book(6,'Nosto', 'Fahim_Vai', 'Shera vai shera 2', 8),
]

@app.get("/books")
async def read_all_books():
    return Books

# without validation
@app.post("/create_book")
async def create_book(book_request= Body()):
    Books.append(book_request)