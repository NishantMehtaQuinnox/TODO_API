from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Tasks as Todo
from models import Base

async_engine = create_async_engine('sqlite+aiosqlite:///D:/python_scripts/Tasks/TODO_API/DB/TODO.db', echo=True, future=True)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class TodoDAL_async:

    def __init__(self):
        self.session = None

    async def init_db(self):
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def connect(self):
        await self.init_db()
        if not self.session:
            self.session = async_session()
        return self.session

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def create_todo(self, title, description):
        async with (await self.connect()) as session:
            new_todo = Todo(title=title, description=description)
            session.add(new_todo)
            await session.commit()
            return new_todo

    async def get_all_todos(self):
        async with (await self.connect()) as session:
            return await session.query(Todo).all()

    async def get_completed_todos(self):
        async with (await self.connect()) as session:
            completed_todos = await session.query(Todo).filter(
                Todo.completed == True).all()
            return completed_todos

    async def get_pending_todos(self):
        async with (await self.connect()) as session:
            pending_todos = await session.query(Todo).filter(
                Todo.completed == False).all()
            return pending_todos

    async def get_todo_by_id(self, todo_id):
        async with (await self.connect()) as session:
            return await session.query(Todo).filter_by(id=todo_id).first()

    async def get_todo(self, query=None):
        async with (await self.connect()) as session:
            if query:
                title_query = query.get("title", "")
                description_query = query.get("description", "")
                todos = await session.query(Todo).filter(
                    (Todo.title.like(f'%{title_query}%'))
                    & (Todo.description.like(f'%{description_query}%'))).all()
            else:
                todos = await session.query(Todo).all()
            return todos

    async def update_todo(self,
                          todo_id,
                          title=None,
                          description=None,
                          completed=None):
        async with (await self.connect()) as session:
            todo = await self.get_todo_by_id(todo_id)
            if not todo:
                return None
            if title:
                todo.title = title
            if description:
                todo.description = description
            if completed is not None:
                todo.completed = completed
            await session.commit()
            return todo

    async def delete_todo(self, todo_id):
        async with (await self.connect()) as session:
            todo = await self.get_todo_by_id(todo_id)
            if not todo:
                return False
            session.delete(todo)
            await session.commit()
            return True
