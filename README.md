# Cortex Code Templates

This repository contains templates for resources (Skills, Agents, Pipelines, etc.) in the Cortex Fabric platform. These
templates are designed to work with the `workspaces` feature of the [Cortex CLI](https://github.com/CognitiveScale/cortex-cli).

Templates are identified by the presence of a `metadata.json` within the folder.

```json
{
    "name": "<template-name>",
    "title": "<template-title>",
    "description": "<template-description>",
    "tags": ["list", "of", "tags", "applied", "to", "template"],
    "enabled": true,
    "resourceType": "Skill"
}
```

The `resourceType` can be one of: `["Skill", "Pipeline"]`.
* Skill templates will have access to the `{{skillname}}` variable in text files, where as `__skillName__` can be used
    in file paths
* Pipeline templates will have access to the `{{pipelinename}}` variable in text files, where as `__pipelineName__` can
  be used in file paths

:warning: **WARNING: The filename must be exactly `metadata.json`, any other variations will be ignored.**
