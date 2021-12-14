"""
Copyright (c) 2021. Cognitive Scale Inc. All rights reserved.

Licensed under CognitiveScale Template/Example Code [License](https://cognitivescale.github.io/cortex-code-templates/LICENSE.md)
"""

import json

if __name__ == '__main__':
    import sys
    params = sys.argv[1]
    params = json.loads(params)
    print(f'Received: {params["payload"]}')
