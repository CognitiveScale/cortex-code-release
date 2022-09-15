# Daemon Skill Example

This workspace template demonstrates a simple daemon skill skeleton that simply returns the payload when invoked.

## Building and Publishing the Skill

### Using the cortex cli

Building skill(s)

```
cortex workspaces build
```

Publishing  skill and docker image

```
cortex workspaces publish
```

### Using the VS code extension (CognitiveScale.cortex-code)

In order to build the daemon skill Docker image, simply select "Build Skills" from the Cortex menu in the IDE.  You can also right-click on the `skill.yaml` file for the skill and select "Build Skill" from the Cortex context menu.

Once the skill is built, you can publish it the same way, by selecting "Publish".
