"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://github.com/CognitiveScale/cortex-code-templates/blob/main/LICENSE.md)
"""

import json
import sys
from cortex.content import ManagedContentClient


# The starting point for the job
if __name__ == '__main__':
    request_body = json.loads(sys.argv[1])
    url = request_body['apiEndpoint']
    token = request_body['token']
    payload = request_body.get('payload', {})

    if payload:
        project_id = payload.get('projectId', request_body['projectId'])

        # Create ManagedContentClient.
        content_client = ManagedContentClient(url=url, token=token, project=project_id)
        key = payload['key']

        # Download data from managed content.
        data = content_client.download(key=key, project=project_id).data
        print(f'Managed Content key {key} is {data}.')
    else:
        print('No payload given')
