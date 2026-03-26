from fastapi.params import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import datetime


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True) # Field means this is a column in the database
    created_at: datetime | None = Field(default_factory = datetime.now) # use .now not .now() cause we wanna call the function each time an object of this class is created
    content: str = Field(index=True) # The actual content of the note

# Postgres configs
postgres_url = "postgresql://jack@localhost/silo"

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session(): # sqlmodel boilerplate to pass of the session parameter to FastAPI
    with Session(engine) as session:
        yield session
