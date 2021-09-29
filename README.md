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
- Download GloVe's general embeddings dictionary from the official site: https://nlp.stanford.edu/projects/glove/ We use Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB download), file name: ```glove.6B.zip```. Unzip the folder and copy the file ```glove.6B.300d.txt``` to the folder where this repository will be cloned.

### Installing

Before starting this tutorial, make sure to have installed the software mentioned in the requirements section.

If it's your first time using our repository, follow these steps:
1. Clone our repository.
2. Open a command-line interpreter and navigate to the folder where this repository is located.
3. Execute the command: ```docker build -t imageName .``` assign a name to the image that will be executed, for example, model-autocompletion. This command will run the content stored in Dockerfile. If it appears ```permissions denied```, execute: ```sudo chmod 666 /var/run/docker.sock```.
4.  Now, if you are running Docker on Linux as your host system, execute: ```docker run -it imageName```. Otherwise, if your host OS is Windows, execute: ```docker run -p 8080:8080 -it imageName```. This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 
5.  To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
6.  To make queries to the local server, open your browser and write the URL that appears inside the command-line interpreter: ![URL server](https://user-images.githubusercontent.com/50658372/127834030-dea9ed89-3651-4a9a-bad1-c25dd88589ae.png) Using the URL in the example, the query will have this structure: ```http://172.17.0.2:8080/model-autocompletion/<model>/<positive_concepts>/<negative_concepts>/<number>/<together>``` Windows users don't have to use the IP shown in the screenshot. Instead, you must write ```localhost```.
  - ```<model>```: you must specify from which model you want our suggestions. Possible values: ```general``` if you want suggestions from the general knowledge, ```contextual``` if you want suggestions from the contextual knowledge, ```general;contextual``` if you want suggestions from both sources of knowledge.
  - ```<positive_concepts>```: here you put the model's slices using the format: slice1term1,slice1term2,slice1term3;slice2term1,slice2term2;slice3term1
  - ```<negative_concepts>```: here you put the historical data (words discarded by the user) using the format: word1,word2,word3...
  - ```<number>```: you specify the number of suggestions you want.
  - ```<together>```: in case you want suggestions from both sources of knowledge, you have to specify here if you want to see the suggestions together or not. Possible values: ```1``` to see the suggestions together, ```0``` to see the suggestions provided by each source of knowledge.
  Example query (Linux users): http://172.17.0.2:8080/model-autocompletion/general;contextual/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Example query (Windows users): http://localhost:8080/model-autocompletion/general;contextual/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Result: ![result](https://user-images.githubusercontent.com/50658372/127837543-9c0a5d91-dc88-41be-b07f-4543b9c7b43a.png)
7. To go out of the internal command-line interpreter type: ```exit```
8. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 

  
  If you already did the steps mentioned before, follow these ones:
 1. If you modified files stored in your local repository, copy them to the container you created before. To do that, execute: ```docker start containerName``` this command will change the container's current status to Up. 
 2. To copy the files to the container: ```docker cp fileName.extension containerID:/fileName.extension```. If you want to know your container's ID, execute the command ```docker ps -a```. This will list your containers and the relevant information like the container ID, name, status...
 3. Now, it's time to run again your container. This time you have to use: ```docker exec -it containerID /bin/bash``` This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 
 4. To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
 5. To make queries do the same as explained in step 6 above.
 6. To go out of the internal command-line interpreter type: ```exit```
 7. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 


## Citations

[1] Loli Burgueño, Robert Clarisó, Sébastien Gérard, Shuai Li, Jordi Cabot: An NLP-Based Architecture for the Autocompletion of Partial Domain Models. CAiSE 2021: 91-106. Preprint: https://hal.archives-ouvertes.fr/hal-03010872/document
