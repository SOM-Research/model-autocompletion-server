# Model Autocompletion (server)

[![License Badge](https://img.shields.io/badge/license-EPL%202.0-brightgreen.svg)](https://opensource.org/licenses/EPL-2.0)

## About

Tool for the autocompletion of partial domain models.

## User guide

### Requirements

- Python version 3
- Java version 8 or greater

### Installing 

1.
2. ...

### Usage

1.  ...


## Developer guide

### Requirements

- You need to install Docker (version 20.10.7) on your computer. Ubuntu users follow this tutorial (steps 1-6): https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 / Windows users follow this tutorial, it may not be available for Windows 10 Home users: https://www.youtube.com/watch?v=5nX8U8Fz5S0 

### Configure Eclipse for client development ?

### Configure Flask server ?

Before starting this tutorial, make sure to have installed the software mentioned in the requirements section.

1. Clone our repository.
2. Open a command-line interpreter and navigate to the folder where this repository is located.
3. Execute the command: "docker build -t imageName ." assign a name to the image that will be executed, for example, model-autocompletion. This command will run the content stored in Dockerfile.
4.  Now, execute: "docker run -it imageName". This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 

## Citations

[1] Loli Burgueño, Robert Clarisó, Sébastien Gérard, Shuai Li, Jordi Cabot: An NLP-Based Architecture for the Autocompletion of Partial Domain Models. CAiSE 2021: 91-106. Preprint: https://hal.archives-ouvertes.fr/hal-03010872/document
