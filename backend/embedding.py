from openai import OpenAI
client = OpenAI()
from schemas import NoteCreate
from sqlmodel import select
from db import Note
from typing import List
from schemas import NoteResponse

def create_embedding(note: NoteCreate):
    text = {'title': note.title,
            'content': note.content}
    response = client.embeddings.create(
        input = str(text),
        model = "text-embedding-3-small"
    )
    embedding = response.data[0].embedding # unpack response object
    return embedding

def get_k_nearest_neighbours(note: NoteCreate, session, k: int = 3) -> List[NoteResponse]: # make sure to handle session when calling
    search_embedding = create_embedding(note)

    knn = Note.embedding.cosine_distance(search_embedding)
    statement = select(Note, knn).order_by(knn).limit(k)
    notes = session.exec(statement)

    return notes.all() # this will print as a list length k of tuples (Note, vector_distance)

