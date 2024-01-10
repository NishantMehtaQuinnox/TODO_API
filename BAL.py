from DAL import TodoDAL

class TodoBAL:
    def __init__(self):
        self.todo_dal = TodoDAL()

    def is_todo_list_empty(self):
        todos = self.todo_dal.get_todo()
        return len(todos) == 0

    def search_todos(self, query):
        return self.todo_dal.get_todo(query)

    def create_todo(self, title, description):
        return self.todo_dal.create_todo(title, description)

    def get_todo_by_id(self, todo_id):
        return self.todo_dal.get_todo_by_id(todo_id)

    def update_todo(self, todo_id, title=None, description=None, completed=None):
        return self.todo_dal.update_todo(todo_id, title, description, completed)

    def delete_todo(self, todo_id):
        return self.todo_dal.delete_todo(todo_id)