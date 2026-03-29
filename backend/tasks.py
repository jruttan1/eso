from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
redis_url = os.getenv('REDIS_URL')

app = Celery("queue", broker=redis_url, backend=redis_url)

@app.task
def embed_note():
    return True
    # To Do: create an embedding function in embeddings.py