from fastapi import FastAPI, HTTPException, Depends
import crud
import db
from contextlib import asynccontextmanager
from schemas import NoteResponse, NoteCreate
from typing import List


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('starting server & db')
    db.create_db_and_tables()
    yield
    print('shutting down server, ending db connection')


app = FastAPI(lifespan=lifespan)


@app.get('/notes', response_model = List[NoteResponse])
async def get_all_notes(session = Depends(db.get_session)): # Depends keyword from fastapi automatically opens and closes the postgres session
    notes = crud.get_all_notes(session) # uses crud functions from crud.py
    return notes
    
@app.get('/notes/{id}', response_model = NoteResponse)
async def get_note_from_id(id: int, session = Depends(db.get_session)):
    note = crud.get_note_from_id(id, session)
    if note is not None:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found in DB")


@app.post('/note', response_model = NoteResponse)
async def add_note(note: NoteCreate, session = Depends(db.get_session)):
    note = crud.write_note(note, session)
    return note

@app.delete('/delete_note/{id}', response_model = NoteResponse)
async def delete_note(id: int, session = Depends(db.get_session)):
    note = crud.delete_note(id, session)
    if note is not None:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found in DB")

@app.put('/update_note/{id}', response_model = NoteResponse)
async def update_note(id: int, note: NoteCreate, session = Depends(db.get_session)):
    note = crud.update_note(id, note, session)
    if note is not None:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found in DB")