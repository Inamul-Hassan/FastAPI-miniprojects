# Book Application

This is a simple Book application built with FastAPI.

## Features

- Retrieve all books
- Retrieve a book by title
- Retrieve books by category
- Retrieve books by author
- Create a new book
- Update an existing book
- Delete a book by title

### Usage

To start the server, navigate into book folder and run:

The application will be available at http://localhost:8000.

API Endpoints

- GET /books: Get all books.
- GET /books/{book_title}: Get a specific book by title.
- GET /books/: Get books by category.
- GET /books/byauthor/{book_author}: Get books by author.
- POST /books/create_book: Create a new book.
- PUT /books/update_book: Update an existing book.
- DELETE /books/delete_book/{book_title}: Delete a book by title.
