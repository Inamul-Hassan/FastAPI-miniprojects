# Todo Application

This is a Todo application built with FastAPI and PostgreSQL.

## Features

- User authentication
- Create, update, delete todos
- Filter todos by owner

### Usage

To start the server, navigate into the todo folder, and run:

```bash
uvicorn main:app --reload
```

The application will be available at http://localhost:8000.

API Endpoints

Auth

- GET /auth/get_users: Get all the users.
- POST /auth/token: Authenticate a user and get a token.
- POST /auth/create_user: Create a new user.

Todo

- GET /todos: Get all todos for the authenticated user.
- GET /todos/{todo_id}: Get a specific todo by ID for the authenticated user.
- POST /todos: Create a new todo for the authenticated user.
- PUT /todos/{todo_id}: Update a specific todo by ID for the authenticated user.
- DELETE /todos/{todo_id}: Delete a specific todo by ID for the authenticated user.

User

- GET /user/me: Get the authenticated user's details.
- PUT /user/change_password: Change the authenticated user's password.
