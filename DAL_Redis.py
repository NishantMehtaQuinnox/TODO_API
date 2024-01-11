import redis
import json

class TodoDALRedis:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis-12453.c325.us-east-1-4.ec2.cloud.redislabs.com', port=12453, decode_responses=True, password="B4AL1yNQ2GlEZcscZSQ3Xnsb3rudV3y7")
        self.todo_key_prefix = 'todo:'

    def create_todo(self, title, description):
        todo_id = self.redis_client.incr('todo_id_counter')
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        new_todo = {'id': todo_id, 'title': title, 'description': description, 'completed': 0}
        self.redis_client.hmset(todo_key, new_todo)
        return new_todo

    def get_all_todos(self):
        todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*')
        todos = [json.loads(self.redis_client.get(todo_key)) for todo_key in todo_keys]
        return todos

    def get_todo_by_id(self, todo_id):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        todo_data = self.redis_client.get(todo_key)
        if todo_data:
            return json.loads(todo_data)
        return None

    def get_todo(self, query=None):
        if query:
            title_query = query.get("title", "")
            description_query = query.get("description", "")
            todo_keys = self.redis_client.keys(f'{self.todo_key_prefix}*')
            todos = [
                json.loads(self.redis_client.get(todo_key))
                for todo_key in todo_keys
                if title_query.lower() in self.redis_client.hget(todo_key, 'title').lower()
                and description_query.lower() in self.redis_client.hget(todo_key, 'description').lower()
            ]
        else:
            todos = self.get_all_todos()
        return todos

    def update_todo(self, todo_id, title=None, description=None, completed=None):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        todo_data = self.redis_client.get(todo_key)
        if not todo_data:
            return None

        todo = json.loads(todo_data)
        if title:
            todo['title'] = title
        if description:
            todo['description'] = description
        if completed is not None:
            todo['completed'] = 0 if completed==False else 1

        self.redis_client.set(todo_key, json.dumps(todo))
        return todo

    def delete_todo(self, todo_id):
        todo_key = f'{self.todo_key_prefix}{todo_id}'
        if not self.redis_client.exists(todo_key):
            return False

        self.redis_client.delete(todo_key)
        return True
