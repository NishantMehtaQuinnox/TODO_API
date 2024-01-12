from DAL import TodoDAL
from DAL_Redis import TodoDALRedis


class TodoBAL:

    def __init__(self, use_redis):
        #self.todo_dal = TodoDAL()
        self.use_redis = use_redis
        self.todo_dal = TodoDALRedis() if use_redis else TodoDAL()

    def is_todo_list_empty(self):
        todos = self.todo_dal.get_todo()
        return len(todos) == 0

    def search_todos(self, query):
        return self.todo_dal.get_todo(query)

    def create_todo(self, title, description):
        return self.todo_dal.create_todo(title, description)

    def get_todo_by_id(self, todo_id):
        return self.todo_dal.get_todo_by_id(todo_id)

    def get_pending_todos(self):
        return self.todo_dal.get_pending_todos()

    def get_completed_todos(self):
        return self.todo_dal.get_completed_todos()

    def update_todo(self,
                    todo_id,
                    title=None,
                    description=None,
                    completed=None):
        return self.todo_dal.update_todo(todo_id, title, description,
                                         completed)

    def delete_todo(self, todo_id):
        return self.todo_dal.delete_todo(todo_id)
