from DAL_async import TodoDAL_async
from DAL_Redis_async import TodoDALRedis_async


class TodoBAL_async:

    def __init__(self, use_redis):
        self.use_redis = use_redis
        self.todo_dal = TodoDALRedis_async() if use_redis else TodoDAL_async()

    async def is_todo_list_empty(self):
        todos = await self.todo_dal.get_todo()
        return len(todos) == 0

    async def search_todos(self, query):
        return await self.todo_dal.get_todo(query)

    async def create_todo(self, title, description):
        return await self.todo_dal.create_todo(title, description)

    async def get_todo_by_id(self, todo_id):
        return await self.todo_dal.get_todo_by_id(todo_id)

    async def get_pending_todos(self):
        return await self.todo_dal.get_pending_todos()

    async def get_completed_todos(self):
        return await self.todo_dal.get_completed_todos()

    async def update_todo(self,
                          todo_id,
                          title=None,
                          description=None,
                          completed=None):
        return await self.todo_dal.update_todo(todo_id, title, description,
                                               completed)

    async def delete_todo(self, todo_id):
        return await self.todo_dal.delete_todo(todo_id)
