"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://github.com/CognitiveScale/cortex-code-templates/blob/main/LICENSE.md)
"""

import json
import sys
from cortex import Cortex


# The starting point for the job
if __name__ == '__main__':
    request_body = json.loads(sys.argv[1])
    url = request_body['apiEndpoint']
    token = request_body['token']
    payload = request_body.get('payload', {})

    if payload:
        project_id = payload.get('projectId', request_body['projectId'])

        # Create ManagedContentClient.
        content_client = Cortex.client(api_endpoint=url, token=token, project=project_id).content
        key = payload['key']

        if payload['command'] == 'download':
            # Download data from managed content.
            data = content_client.download(key=key, project=project_id).data
            print(f'{data}')

        elif payload['command'] == 'upload':
            # Uploads string to managed content
            content = payload['content']
            content_client.upload(key=key, project=project_id, stream_name=key, stream=content,
                                  content_type="application/octet-stream")

            print(f'Managed content ({key}) uploaded: {content}')
        else:
            print('Invalid command given. Valid commands: `download`, `upload`')
    else:
        print('No payload given')
