"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://github.com/CognitiveScale/cortex-code-templates/blob/main/LICENSE.md)
"""

from fastapi import FastAPI
from cortex import Cortex

app = FastAPI()


@app.post('/invoke')
def run(request_body: dict):
    url = request_body['apiEndpoint']
    token = request_body['token']
    payload = request_body.get('payload', {})

    if payload:
        project_id = payload.get('projectId', request_body['projectId'])

        content_client = Cortex.client(api_endpoint=url, token=token, project=project_id).content
        key = payload['key']
        modifier = int(payload['modifier'])
        operator = payload['command']

        # Upload managed content with 0 value if key doesnt exist
        if not content_client.exists(key, project_id):
            content_client.upload(key=key, project=project_id, stream_name=key, stream="0",
                                  content_type="application/octet-stream")

        # Download current value from managed content.
        current_value = int(content_client.download(key=key, project=project_id).data)
        
        # Calculate modified_value
        if operator == '+':
            modified_value = current_value + modifier
        elif operator == '-':
            modified_value = current_value - modifier
        elif operator == '*':
            modified_value = current_value * modifier
        elif operator == '/':
            modified_value = current_value / modifier
        else:
            return {'payload': {"message": "Invalid command. Valid commands: `+`, `-`, `*`, `/`."}}
    else:
        return {'payload': {"message": "No payload given"}}

    # Upload modified_value to managed content
    content_client.upload(key=key, project=project_id, stream_name=key, stream=str(modified_value),
                                    content_type="application/octet-stream")

    return {'payload': {"statement": f'{current_value}{payload["command"]}{modifier}={modified_value}',
                        "message": f'{modified_value} saved in key {key}'}}
