from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

todos = [
    {"id": 1, "description": "Do something", "completed": True},
    {"id": 2, "description": "Do something else", "completed": False},
    {"id": 3, "description": "Do something again", "completed": False}
]


@app.get("/", response_class=HTMLResponse)
async def get_todos(request: Request):
    return templates.TemplateResponse("pages/todos.html", {"request": request, "todos": todos})


@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, description: Annotated[str, Form()]):
    todos.append({"id": todos[-1]["id"]+1, "description": description, "completed": False})
    return templates.TemplateResponse("components/todo-list.html", {"request": request, "todos": todos})


@app.put("/todos/{id}", response_class=HTMLResponse)
async def update_todo_status(request: Request, id: int):
    todo = next(todo for todo in todos if todo["id"] == id)
    todo["completed"] = not todo["completed"]
    return templates.TemplateResponse("components/todo-item.html", {"request": request, "todo": todo})


@app.delete("/todos/{id}", response_class=HTMLResponse)
async def delete_todo_status(request: Request, id: int):
    todos[:] = [todo for todo in todos if todo.get("id") != id]
    return "" # Return empty string because we are deleting the todo from the list


@app.delete("/todos", response_class=HTMLResponse)
async def delete_all_todos(request: Request, selected_todo_items: list[int] = Form()):
    todos[:] = [todo for todo in todos if todo.get("id") not in selected_todo_items]
    return templates.TemplateResponse("components/todo-list.html", {"request": request, "todos": todos})