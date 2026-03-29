from openai import OpenAI
client = OpenAI()
from schemas import NoteCreate

def create_embedding(note: NoteCreate):
    text = {'title': note.title,
            'content': note.content}
    embedding = client.embeddings.create(
        input = str(text),
        model = "text-embedding-3-small"
    )
    return embedding