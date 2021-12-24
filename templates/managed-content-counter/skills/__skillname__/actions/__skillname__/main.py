"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://github.com/CognitiveScale/cortex-code-templates/blob/main/LICENSE.md)
"""

from fastapi import FastAPI
from cortex.content import ManagedContentClient

app = FastAPI()


@app.post('/invoke')
def run(request_body: dict):
    url = request_body['apiEndpoint']
    token = request_body['token']
    payload = request_body.get('payload', {})

    if payload:
        project_id = payload.get('projectId', request_body['projectId'])

        # Create ManagedContentClient.
        content_client = ManagedContentClient(url=url, token=token, project=project_id)
        key = payload['key']
        modifier = payload['modifier']

        # Download current value from managed content.
        current_value = content_client.download(key=key, project=project_id).data
        modified_value = current_value

        # Calculate modified_value
        if payload['command'] == 'add':
            modified_value = current_value + modifier
        elif payload['command'] == 'subtract':
            modified_value = current_value - modifier
        elif payload['command'] == 'multiply':
            modified_value = current_value * modifier
        elif payload['command'] == 'divide':
            modified_value = current_value / modifier
        else:
            return {'payload': {"message": "Invalid command. Valid commands: `add`, `subtract`, `multiply`, `divide`."}}
    else:
        return {'payload': {"message": "No payload given"}}

    operators = {"add": "+", "subtract": "-", "multiply": "×", "divide": "/"}
    return {'payload': {"statement": f'{current_value}{operators["command"]}{modifier}={modified_value}',
                        "message": f'`{modified_value}` saved in key {key}'}}
