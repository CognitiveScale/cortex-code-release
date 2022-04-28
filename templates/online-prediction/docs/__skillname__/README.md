### Online Prediction Skill

Long running Cortex skill serving REST API prediction requests

Note:
> This project assumes a `fast api server` with one endpoint `/invoke` that is run with the Uvicorn python3 binary; you may change to another framework or language.

## Files Generated
- `docs/{{skillname}}/README.md`: Provide the objectives, requirements, and instructions for the Skill here.
- `skills/{{skillname}}/actions/{{skillname}}/Dockerfile`: Modify this to build the Docker image for the action
  `skills/{{skillname}}/actions/{{skillname}}/main.py`: Modify the code in this file for the daemon
  `skills/{{skillname}}/actions/{{skillname}}/requirements.txt`: List all the dependencies and libraries needed for this Skill
  `skills/{{skillname}}/actions/{{skillname}}/invoke/request/message.json`: A test JSON payload to invoke the Skill
  `skills/{{skillname}}/actions/{{skillname}}/skill.yaml`: Skill definition for the daemon

## Building and Publishing the Skill

In order to build the daemon skill Docker image, simply select "Build Skills" from the Cortex menu in the IDE.  You can also right-click on the `skill.yaml` file for the skill and select "Build Skill" from the Cortex context menu.

Once the skill is built, you can publish it the same way, by selecting "Publish".



#### Files
* `skill.yaml` Skill definition
* `predict/main.py` Python3 code serving the daemon API
* `train/main.py` Example Python3 code for training the model
* `requirements.txt` Python3 libraries dependencies
* `Dockerfile` to build Docker image for this skill

