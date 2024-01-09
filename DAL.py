from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Tasks as Todo

engine = create_engine('sqlite:///D:/python_scripts/Tasks/TODO_API/DB/TODO.db', echo=True)
Base = declarative_base()

Base.metadata.create_all(engine)

class TodoDAL:
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def create_todo(self, title, description):
        new_todo = Todo(title=title, description=description)
        self.session.add(new_todo)
        self.session.commit()
        return new_todo

    def get_all_todos(self):
        return self.session.query(Todo).all()

    def get_todo_by_id(self, todo_id):
        return self.session.query(Todo).filter_by(id=todo_id).first()

    def get_todo(self, query=None):
        if query:
            todos = self.session.query(Todo).filter(
                (Todo.title.like(f'%{query}%')) | (Todo.description.like(f'%{query}%'))
            ).all()
        else:
            todos = self.get_all_todos()
        return todos
    
    def update_todo(self, todo_id, title=None, description=None, completed=None):
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return None
        if title:
            todo.title = title
        if description:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        self.session.commit()
        return todo

    def delete_todo(self, todo_id):
        todo = self.get_todo_by_id(todo_id)
        if not todo:
            return False
        self.session.delete(todo)
        self.session.commit()
        return True