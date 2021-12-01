# Need to import packages to handle json and running the daemon
import json
from fastapi import FastAPI

# Initialize daemon server to listen for routes
app = FastAPI()


# GET /hello : A health check. Returns a basic hello message. No payload is needed
@app.get('/hello')
def hello():
    return {'message': 'Hello from {{skillname}} GET'}


# POST /invoke : Returns the word count of the text in the payload.
@app.post('/invoke')
def invoke(request_body: dict):
    if request_body:
        payload = request_body.get('payload', {})
        text = payload.get('text', '')
        word_count = len(text.split())
        return {"payload": {"message": f'Hello received: \'{text}\', word count: {word_count}'}}
