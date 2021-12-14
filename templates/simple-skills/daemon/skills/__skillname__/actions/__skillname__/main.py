"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://cognitivescale.github.io/cortex-code-templates/LICENSE.md)
"""

from fastapi import FastAPI

app = FastAPI()


@app.post('/invoke')
def run(request_body: dict):
    payload = request_body['payload']
    return {'payload': payload}
