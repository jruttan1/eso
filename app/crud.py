from sqlmodel import Session, select
from db import Note

def get_all_notes(session: Session):
    statement = select(Note)
    notes = session.exec(statement)
    return notes

def get_note_from_id(id: int, session: Session):
    statement = select(Note).where(Note.id == id)
    note = session.exec(statement).first() # this is not the same as python exec builtin, this just runs the query in the postgres session
    return note

def write_note(content: str, session: Session):
    note = Note(content = content) # Id default field auto assigns on object creation in db
    session.add(note)
    session.commit()
    session.refresh(note) #refreshes local object to have id and datetime from postgres (basically pull from db after pushing) to give id to return statement below
    return note

