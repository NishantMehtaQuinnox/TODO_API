import redis.asyncio

class TodoDALRedis_async:

    def __init__(self):
        self.redis_client = redis.from_url(url="redis://redis-18552.c267.us-east-1-4.ec2.cloud.redislabs.com",port=18552,password='jdj3wE7esEVxsK9CQ1f3Z74nwBqY8wN2',decode_responses=True)
        self.todo_key_prefix = 'todo:'

    async def create_todo(self, title, description):
        todo_id = self.redis_client.incr('todo_id_counter')
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        new_todo = {
            'id': todo_id,
            'title': title,
            'description': description,
            'completed': 0
        }
        self.redis_client.hmset(todo_key, new_todo)
        return new_todo

    async def get_all_todos(self):
        todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*')
        todos = [
            self.redis_client.hgetall(todo_key) for todo_key in todo_keys
        ]
        return todos

    async def get_completed_todos(self):
        todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*')
        completed_todos = [
            self.redis_client.hgetall(todo_key) for todo_key in todo_keys
            if self.redis_client.hget(todo_key, 'completed') == '1'
        ]
        return completed_todos

    async def get_pending_todos(self):
        todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*')
        completed_todos = [
            self.redis_client.hgetall(todo_key) for todo_key in todo_keys
            if self.redis_client.hget(todo_key, 'completed') == '0'
        ]
        return completed_todos

    async def get_todo_by_id(self, todo_id):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        todo_data = self.redis_client.hgetall(todo_key)
        if todo_data:
            return todo_data
        return None

    async def get_todo(self, query=None):
        if query:
            title_query = query.get("title", "")
            description_query = query.get("description", "")
            todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*'
                                                     )
            todos = [
                self.redis_client.hgetall(todo_key)
                for todo_key in todo_keys if title_query.lower() in (
                    self.redis_client.hget(todo_key, 'title')).lower()
                and description_query.lower() in (self.redis_client.hget(
                    todo_key, 'description')).lower()
            ]
        else:
            todos = await self.get_all_todos()
        return todos

    async def update_todo(self,
                          todo_id,
                          title=None,
                          description=None,
                          completed=None):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        todo_data = self.redis_client.hgetall(todo_key)
        if not todo_data:
            return None

        if title:
            self.redis_client.hset(todo_key, 'title', title)
        if description:
            self.redis_client.hset(todo_key, 'description', description)
        if completed is not None:
            self.redis_client.hset(todo_key, 'completed',
                                         '0' if completed == False else '1')

        updated_todo = self.redis_client.hgetall(todo_key)
        return updated_todo

    async def delete_todo(self, todo_id):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        if not self.redis_client.exists(todo_key):
            return False

        self.redis_client.delete(todo_key)
        return True
