from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app= FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int
    def __init__(self, id, title, author, description , rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create',default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=0, le=5)
    published_date: int= Field(ge=1950, le=2030)
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "title":"A new title",
                "author":"A new author",
                "description":"A new description of the book",
                "ratings":5,
                "published_date": 2013
            }
        }
    }
    
BOOKS = [
    Book(1, "coding with Hisham", "Hisham Shaaban", "A very nice book", 5,2022),
    Book(2, "Be fast with FastAPI", "Hisham Shaaban", "A great book", 5,1995),
    Book(3, "Master Endpoints", "Hisham Shaaban", "A awesome book", 5,2005),
    Book(4, "HP1", "Author 1", "Book description", 2,2011),
    Book(5, "HP2", "Author 2", "Book description", 3,1980),
    Book(6, "HP3", "Author 3", "Book description", 1,2022),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


        
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_date(book_return:int = Query(ge=1950, le=2030)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_return:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/by_rating", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_return: int = Query(ge=0, le=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_return:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int =Path(gt=0) ):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id +1
    return book

@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_updated = True
            return book
    if not book_updated:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int = Path(gt=0)):
    book_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_updated = True
            break
    if not book_updated:
        raise HTTPException(status_code=404, detail="Item not found")