# Cortex Code Templates repository

This repository contains the current release of the Cortex Visual Studio Code plugin generator templates.


## Templates

### Simple Skills

| Folder                                                     | Language | Description                                                                                                                                                   |
|------------------------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [simple-skills/daemon](./simple-skills/daemon)             | Python   | A system generated Skill based on the custom daemon Skill template.                                                                                           |
| [simple-skills/external-api](./simple-skills/external-api) | Python   | A system generated Skill based on the custom external API Skill template. This skill type allows users to wrap an external REST API as a Cortex Fabric Skill. |
| [simple-skills/job](./simple-skills/job)                   | Python   | A system generated Skill based on the custom job Skill template.                                                                                              |


## Examples

| Folder                                   | Language | Description                                                                                                                                             |
|------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| [simple-experiment](./simple-experiment) | Python   | A pair of Skills that train (job) and predict (daemon) a Model using sklearn's RandomForestClassifier and the cortex-python library's Experiment class. |
| [word-count-agent](./word-count-agent)   | Python   | An Agent with one daemon-Skill that reads `text` from the payload and responds with a word count.                                                       |


## Documentation

[Develop Skills](https://cognitivescale.github.io/cortex-fabric/docs/build-skills/define-skills)
[Cortex Visual Studio Code Extension](https://cognitivescale.github.io/cortex-code/)
