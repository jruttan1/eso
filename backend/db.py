from fastapi.params import Depends
from sqlmodel import Field, AsyncSession, SQLModel, create_async_engine
from datetime import datetime


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True) # Field means this is a column in the database
    created_at: datetime = Field(default_factory = datetime.now) # use .now not .now() cause we wanna call the function each time an object of this class is created
    content: str # The actual content of the note

# Indexing is a way to optimize database queries. When you create an index on a column, 
# the database creates a data structure that allows it to quickly locate rows based on 
# the values in that column. This speeds up query performance, especially for large datasets.
# for this db we likely dont need any indexing but i'll do it for title just to experiment


# Postgres configs
postgres_url = "postgresql://jack@localhost/silo"

engine = create_async_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

async def get_session(): # sqlmodel boilerplate to pass of the session parameter to FastAPI
    async with AsyncSession(engine) as session:
        yield session
