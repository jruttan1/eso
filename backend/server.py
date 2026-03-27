from fastapi import FastAPI, HTTPException, Depends
import crud
import db


app = FastAPI()

@app.get('/notes')
async def get_all_notes(session = Depends(db.get_session)): # Depends keyword from fastapi automatically opens and closes the postgres session
    notes = await crud.get_all_notes(session) # uses crud functions from db
    return notes

@app.get('/notes/{id}')
async def get_note_from_id(id: int, session = Depends(db.get_session)):
    note = await crud.get_note_from_id(id, session)
    if note is not None:
        return note
    else:
        raise HTTPException(status_code=404, detail="Note not found in DB")


@app.post('/note')
async def update_content(content: str, title: str, session = Depends(db.get_session)):
    note = await crud.write_note(content, title, session)
    return note
