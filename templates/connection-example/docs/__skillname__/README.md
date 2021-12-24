# {{skillnamee}} Connection Example (UPDATE THIS FOR YOUR SKILL)

Cortex Skill (daemon) example for Cortex Connections. This demonstrates:
* Create Cortex Connections with Secrets
    * In the Cortex project, create Secrets `test-db-uri`, `test-db-name` and `test-db-collection` as per MongoDB server details
    * Create Cortex Connection (of type MongoDB) from Connection definition (test-connection.json), using `cortex connections save test-connection.json` command
* Use Connections in Skill
    * See `main.py` for how to use Cortex Connections in a Skill. This will create a connection and pool it for serving subsequent queries.  
    * Create Secrets and run `make all` to save connection, build & deploy Action/Skill, and test the deployed Skill 
> Modify these sections for your specific use case.

## Files Generated
- `connections/` - The directory that houses the Connections
  - `connection.json` - The connection to be used to connect to Mongo.
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

### Run the daemon
```shell
uvicorn main:app --port 5000

INFO:     Started server process [57435]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

### Test daemon endpoint

This can be done several ways. Use your preferred method to test the endpoint locally.

#### a. Using curl
```shell
curl -X 'POST' \
  'http://localhost:5000/invoke' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"payload": {"message":  "This is a test payload message"}}'
````

Response:
```json
{
  "message":  "This is a test payload message"
}
```
