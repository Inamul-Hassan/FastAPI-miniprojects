from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title two', 'author': 'Author two', 'category': 'science'},
    {'title': 'Title three', 'author': 'Author three', 'category': 'history'},
    {'title': 'Title four', 'author': 'Author four', 'category': 'math'},
    {'title': 'Title five', 'author': 'Author two', 'category': 'math'},
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    book = next((book for book in BOOKS
                 if book['title'].casefold() == book_title.casefold()), None)
    if book is not None:
        return book
    else:
        return {'error': 'Book not found'}


@app.get("/books/")
async def read_category_by_query(category: str):
    books = [book for book in BOOKS
             if book['category'].casefold() == category.casefold()]
    if books:
        return books
    else:
        return {'error': 'Category not found'}


@app.get("/books/byauthor/{book_author}")
async def read_book_by_author(book_author: str):
    books = [book for book in BOOKS
             if book.get('author').casefold() == book_author.casefold()]
    if books:
        return books
    else:
        return {'error': 'Author not found'}


@app.get("/books/{book_author}/")
async def read_author_by_query(book_author: str, category: str):
    print(book_author)
    print(category)
    books = [book for book in BOOKS
             if book['author'].casefold() == book_author.casefold() and
             book['category'].casefold() == category.casefold()]
    if books:
        return books
    else:
        return {'error': 'Author not found'}


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
