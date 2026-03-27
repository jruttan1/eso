from sqlmodel import AsyncSession, select
from db import Note

async def get_all_notes(session: AsyncSession):
    statement = select(Note)
    notes = await session.exec(statement)
    return notes

async def get_note_from_id(id: int, session: AsyncSession): 
    statement = select(Note).where(Note.id == id)
    note = await session.exec(statement) # this is not the same as python exec builtin, this just runs the query in the postgres session
    return note.first() # unpack container to return one object

async def write_note(content: str, title: str, session: AsyncSession):
    note = Note(content = content, title = title) # Id default field auto assigns on object creation in db
    session.add(note)
    await session.commit()
    await session.refresh(note) #refreshes local object to have id and datetime from postgres (basically pull from db after pushing) to give id to return statement below
    return note

