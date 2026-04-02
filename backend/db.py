from sqlmodel import Field, SQLModel, Session, create_engine, Relationship
from datetime import datetime
import os
from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column
from typing import List, Optional
class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True) # Field means this is a column in the database
    created_at: datetime = Field(default_factory = datetime.now) # use .now not .now() cause we wanna call the function each time an object of this class is created
    updated_at: datetime = Field(default_factory = datetime.now)
    content: str # The actual content of the note
    embedding: list | None = Field(sa_column = Column(Vector(1536), nullable = True))


class Edge(SQLModel, table=True):
    from_note_id: int | None = Field(default = None, foreign_key = "note.id", primary_key = True)
    to_note_id: int | None = Field(default = None, foreign_key = "note.id", primary_key = True)
    distance: float | None # cosine distance between 2 notes


class Cluster(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key = True)
    cluster_name: str | None

class NoteCluster(SQLModel, table=True): # junction table to represent the many-many relationship
    note_id: int | None = Field(foreign_key="note.id", primary_key=True)
    cluster_id: int | None = Field(foreign_key ="cluster.id", primary_key= True)


# Postgres configs
load_dotenv()
postgres_url = os.getenv('POSTGRES_URL')

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session(): # sqlmodel boilerplate to pass of the session parameter to FastAPI
    with Session(engine) as session:
        yield session