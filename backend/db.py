from sqlmodel import Field, SQLModel, Session, create_engine
from datetime import datetime
import os
from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True) # Field means this is a column in the database
    created_at: datetime = Field(default_factory = datetime.now) # use .now not .now() cause we wanna call the function each time an object of this class is created
    updated_at: datetime = Field(default_factory = datetime.now)
    content: str # The actual content of the note
    embedding: list | None = Field(sa_column = Column(Vector(1536), nullable = True))

# Indexing is a way to optimize database queries. When you create an index on a column, 
# the database creates a data structure that allows it to quickly locate rows based on 
# the values in that column. This speeds up query performance, especially for large datasets.
# for this db we likely dont need any indexing but i'll do it for title just to experiment

# Postgres configs
load_dotenv()
postgres_url = os.getenv('POSTGRES_URL')

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session(): # sqlmodel boilerplate to pass of the session parameter to FastAPI
    with Session(engine) as session:
        yield session