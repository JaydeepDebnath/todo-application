from app.models import Todo
from app import db

def resolve_todos(root, info):
    return Todo.query.all()

def resolve_todo(root, info, id):
    return Todo.query.get(id)

def todo_creation(root, info, title = None,description=None,createdAt = None,updatedAt = None):
    new_todo = Todo(title=title,description=description,createdAt=createdAt,updatedAt=updatedAt)
    db.session.add(new_todo)
    db.session.commit()
    
    return new_todo

def update_todo(root,info,id,title=None,description=None,createdAt = None,updatedAt = None):
    todo = Todo.query.get(id)

    if not todo:
        return None
    
    if title:
        todo.title = title
    if description:
        todo.description = description
    if createdAt:
        todo.createdAt = createdAt
    if updatedAt:
        todo.updatedAt = updatedAt

    db.session.commit()
    return todo

def delete_todo(root,info,id):
    todo = Todo.query.get(id)
    if not todo:
        return None
    
    db.session.delete(todo)
    db.session.commit()
    return todo