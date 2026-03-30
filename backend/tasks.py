from celery import Celery
from dotenv import load_dotenv
import os
from embedding import create_embedding, get_k_nearest_neighbours
from schemas import NoteCreate, NoteResponse
from sqlmodel import Session
from db import engine, Edge
from crud import get_note_from_id

load_dotenv()
redis_url = os.getenv('REDIS_URL')

app = Celery("queue", broker=redis_url, backend=redis_url)

@app.task
def embed_note(id: int) -> NoteResponse:
    with Session(engine) as session: # start db session for this task

        note = get_note_from_id(id, session) # pull the note you wanna update
        embedding = create_embedding(note) # call create embedding, returns a list of vectors
        note.embedding = embedding # add it to the note object

        session.add(note)
        session.commit()
        session.refresh(note)

        find_similar.delay(id)
    
        return note
    
@app.task
def find_similar(id: int):
    with Session(engine) as session:

        note = get_note_from_id(id, session)
        similar = get_k_nearest_neighbours(note, session) # pass k if you want more or less than 5 similar

        connect_similar.delay(id, similar)
        return similar
    

@app.task
def connect_similar(id: int, similar_notes):
    with Session(engine) as session:

        for note in similar_notes:
            similar_note, distance = note
            edge = Edge(from_note_id = id, to_note_id = similar_note.id, distance = distance)
            session.add(edge)
            session.commit()
            session.refresh(edge)

        return edge
    
