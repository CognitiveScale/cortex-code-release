# {{skillname}} Managed Content Example (UPDATE THIS FOR YOUR SKILL)

`{{skillname}}` uploads and downloads Managed Content.

> Modify these sections for your specific use case.

## Included Files to Review
- `docs/` - The directory that houses the Skills' READMEs
    - `{{skillname}}/`: The directory that houses the {{skillname}} Skill's README
        - `README.md`: Provides the objectives, requirements, and instructions for generating and deploying the Skill.
- `skills/`: The directory that houses the Skills
    - `{{skillname}}/`: The directory that houses the {{skillname}} Skill's assets
        - `actions/`: The directory that houses the {{skillname}} Skill's Actions
            - `{{skillname}}/`: The contents of the {{skillname}} action
                - `Dockerfile`: Builds the Docker image the action
                - `main.py`: Code for Cortex job
                - `requirements.txt`: Dependencies and libraries
        - `invoke/`: Contains the payloads, organized by Skill input name, used to invoke the {{skillname}} Skill
            - `request/`: Contains payload files used to invoke the Skill
                - `message-download.json`: JSON payload used to invoke the Skill. Uploads content to managed content
                - `message-upload.json`: JSON payload used to invoke the Skill. Downloads content from managed content
        - `skill.yaml`: {{skillname}} Skill definition and Action mapping
            

## Generate the Skill

You've already done this via:
- [VS Code Extension](https://cognitivescale.github.io/cortex-code/)
- [Skill Builder in the Fabric Console](https://cognitivescale.github.io/cortex-fabric/docs/build-skills/skill-builder-ui)

Please use the above links for more information on how to continue building, pushing, deploying, developing, and invoking your Skill.

> NOTE: Modify the following files for your specific use case:
> - `docs/{{skillname}}/README.md`
> - `skills/{{skillname}}/actions/{{skillname}}/Dockerfile`
> - `skills/{{skillname}}/actions/{{skillname}}/main.py`
> - `skills/{{skillname}}/actions/{{skillname}}/requirements.txt`
> - `skills/{{skillname}}/actions/skill.yaml`
> - `invoke/request/message-download.json`
> - `invoke/request/message-upload.json`


## Test the code locally
To avoid using up your private registry space, it is good practice testing your code before pushing.

Create Python virtual env.
```shell
python -m venv testvenv
source testvenv/bin/activate
pip install -r ./skills/{{skillname}}/requirements.txt
```

Testing the `upload` Managed Content code path of the Job.
```shell
python ./skills/{{skillname}}/main.py '{"apiEndpoint":"https://api.dci-dev.dev-eks.insights.ai", 
"projectId":"cogu", "token":"xxxx", 
"payload":{"command":"upload", "key":"{{skillname}}-content", "content":"I am here"}}'
````
Response:
```text
Managed content ({{skillname}}-content) uploaded: I am here
```

Testing the `download` Managed Content code path of the Job.
```shell
python ./skills/{{skillname}}/main.py '{"apiEndpoint":"https://api.dci-dev.dev-eks.insights.ai", 
"projectId":"cogu", "token":"xxxx", 
"payload":{"command":"download", "key":"{{skillname}}-content"}}'
````
Response:
```text
b'I am here'
```

## Documentation
- [Cortex Fabric Documentation - Development - Develop Skills](https://cognitivescale.github.io/cortex-fabric/docs/development/define-skills)
- [Skill Elements](https://cognitivescale.github.io/cortex-fabric/docs/build-skills/define-skills#skill-elements)
- 
