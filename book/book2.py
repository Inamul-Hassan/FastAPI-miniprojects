from typing import Optional
from fastapi import Body, FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=2)
    description: str = Field(min_length=5, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=0, lt=2025)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Book_title",
                "author": "Author of the book",
                "description": "Description of the book",
                "rating": 5,
                "published_date": 2023
            }
        }


BOOKS = [
    Book(1, "It Ends With Us", "Colin Hower", "Romance at its best", 5, 2020),
    Book(2, 'Ugly Love', 'Colin Hower', 'unknow', 3, 2015),
    Book(3, 'It Starts with us', 'Colin Hower',
         'prequel to It Ends with us', 4, 2018),
    Book(4, 'New Book 1', "New Author 1", 'Unknown description', 1, 2019),
    Book(5, 'New Book 2', "New Author 2", 'Unknown description', 2, 2021),
    Book(6, 'New Book 3', "New Author 2", 'Unknown description', 3, 2022)
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get('/books/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books = [book for book in BOOKS
             if book.rating == rating]
    return books


@app.get('/books/publish/', status_code=status.HTTP_200_OK)
async def read_book_by_publish_date(published_date: int = Query(gt=0, lt=2025)):
    books = [book for book in BOOKS
             if book.published_date == published_date]
    return books


@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    book = Book(**new_book.model_dump())
    book = id_generator(book)
    print(new_book.model_dump())
    print(book)
    BOOKS.append(book)


@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(update_book: BookRequest):
    book_changed: bool = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == update_book.id:
            BOOKS[i] = update_book
            book_changed = True
    print(BOOKS)
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete('/books/delete_book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed: bool = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    print(BOOKS)
    if not book_changed:
        raise HTTPException(status_code=404, detail="Book not found")


def id_generator(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
