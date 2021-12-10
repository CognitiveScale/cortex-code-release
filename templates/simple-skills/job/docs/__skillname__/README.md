# {{skillname}} Job Skill (UPDATE THIS FOR YOUR SKILL)

A system generated Skill based on the custom job Skill template.

> Modify these sections for your specific use case.

## Files Generated
- `docs/` - The directory that houses the Skills' READMEs
    - `{{skillname}}/`: The directory that houses the {{skillname}} Skill's README
        - `README.md`: Provide the objectives, requirements, and instructions for generating and deploying the Skill here.
- `skills/`: The directory that houses the Skills
    - `{{skillname}}/`: The directory that houses the {{skillname}} Skill's assets
        - `actions/`: The directory that houses the {{skillname}} Skill's Actions
            - `{{skillname}}/`: The contents of the {{skillname}} action
                - `Dockerfile`: Modify this to build the Docker image the action
                - `main.py`: Modify the code in this file for your Cortex job
                - `requirements.txt`: List all the dependencies and libraries needed for this Skill
        - `invoke/`: Contains the payloads, organized by Skill input name, used to invoke the {{skillname}} Skill
            - `request/`: Contains payload files used to invoke the Skill
                - `message.json`: Write a test JSON payload to invoke the Skill
            - `skill.yaml`: Define {{skillname}} Skill definition and map Actions here



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
> - `invoke/request/message.json`

## Test the code locally

To avoid filling your private registry, testing your code prior to deployment is recommended. Here's a way to do that.

### Create Python virtual env
```shell
python -m venv testvenv
source testvenv/bin/activate
pip install -r requirements.txt
```

### Test the job
```shell
python ./main.py '{"payload":{"message":  "This is a test payload message"}}'
````
Response:
```text
{"message":  "This is a test payload message"}
```

## Documentation
- [Cortex Fabric Documentation - Development - Develop Skills](https://cognitivescale.github.io/cortex-fabric/docs/development/define-skills)
- [Skill Elements](https://cognitivescale.github.io/cortex-fabric/docs/build-skills/define-skills#skill-elements)
- 