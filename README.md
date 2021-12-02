# Model Autocompletion (server)

[![License Badge](https://img.shields.io/badge/license-EPL%202.0-brightgreen.svg)](https://opensource.org/licenses/EPL-2.0)

## About

Tool for the autocompletion of partial domain models.

## User guide

### Requirements (local mode)

- You need to install Docker (version 20.10.7) on your computer. Ubuntu users follow this tutorial (steps 1-6): https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 / Windows users follow this tutorial. Windows 10 Home users should install Docker Desktop as  mentioned in this video: https://www.youtube.com/watch?v=5nX8U8Fz5S0. In case Windows 10 Home users experience some WSL errors, please check this page: https://docs.docker.com/desktop/windows/wsl/ in the prerequisites section the second point explains how to solve WSL errors.
- Download GloVe's general embeddings dictionary from the official site: https://nlp.stanford.edu/projects/glove/ We use Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB download), file name: ```glove.6B.zip```. Unzip the folder and copy the file ```glove.6B.300d.txt``` to the folder where this repository will be cloned.

### Installing (local mode)

If it's your first time using our repository, follow these steps:
Before starting, Windows users should run Docker Desktop first. 
1. Clone our repository.
2. Open a command-line interpreter and navigate to the folder where this repository is located.
3.  It is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/files/'
4. Execute the command: ```docker build -t imageName .``` assign a name to the image that will be executed, for example, model-autocompletion. This command will run the content stored in Dockerfile. If it appears ```permissions denied```, execute: ```sudo chmod 666 /var/run/docker.sock```.
5.  Now, if you are running Docker on Linux as your host system, execute: ```docker run -it imageName```. Otherwise, if your host OS is Windows, execute: ```docker run -p 8080:8080 -it imageName```. This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile).
6.  To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
7.  To make queries to the local server, open your browser and write the URL that appears inside the command-line interpreter: ![URL server](https://user-images.githubusercontent.com/50658372/127834030-dea9ed89-3651-4a9a-bad1-c25dd88589ae.png) Using the URL in the example, the query will have this structure: ```http://172.17.0.2:8080/model-autocompletion/<model>/<positive_concepts>/<negative_concepts>/<number>/<together>``` Windows users don't have to use the IP shown in the screenshot. Instead, you must write ```localhost```.
  - ```<model>```: you must specify from which model you want our suggestions. Possible values: ```general``` if you want suggestions from the general knowledge, ```contextual``` if you want suggestions from the contextual knowledge, ```general;contextual``` if you want suggestions from both sources of knowledge.
  - ```<positive_concepts>```: here you put the model's slices using the format: slice1term1,slice1term2,slice1term3;slice2term1,slice2term2;slice3term1
  - ```<negative_concepts>```: here you put the historical data (words discarded by the user) using the format: word1,word2,word3...
  - ```<number>```: you specify the number of suggestions you want.
  - ```<together>```: in case you want suggestions from both sources of knowledge, you have to specify here if you want to see the suggestions together or not. Possible values: ```1``` to see the suggestions together, ```0``` to see the suggestions provided by each source of knowledge.
  Example query (Linux users): http://172.17.0.2:8080/model-autocompletion/general/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Example query (Windows users): http://localhost:8080/model-autocompletion/general/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Result: ![Result](https://user-images.githubusercontent.com/50658372/144405246-2aa19023-8ba6-4afc-94ad-dc204ffdb150.png)
7. To go out of the internal command-line interpreter type: ```exit```
8. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 

### Usage (local mode)

If you already did the steps mentioned in the previous section, follow these ones:
Before running the container and the server, it is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/files/'
 1. Run your container. This time you have to use: ```docker exec -it containerID /bin/bash``` This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 
 2. To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
 3. To make queries do the same as explained in step 6 above.
 4. To go out of the internal command-line interpreter type: ```exit```
 5. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 


### Requirements (remote mode)

- You need to install an open-source terminal emulator, serial console. There are a lot, in this example, we will use  PuTTY a free SSH and telnet client https://www.putty.org/
- You need a user with sudo or admin priviledges.
- Install python and flask (see the information inside requirements.txt file), gcc, make and git. 

### Installing (remote mode)

1. Open PuTTY SSH Client.
2. Create a new SSH session introducing the host name and the port. In this example we have used as host name and port the following ones:
![Host name and port](https://user-images.githubusercontent.com/50658372/144410647-3a426339-384f-40e0-ab61-6ca9ff54e7e2.png)
3. Click Open. 
4. You will be required to enter a password. Write it and press Enter.
![Login](https://user-images.githubusercontent.com/50658372/144417130-1388ef74-bdd3-43fa-8fc6-77f96971967b.png)
5. Now it will appear a basic CLI.
![Console](https://user-images.githubusercontent.com/50658372/144417183-25df1659-1a31-412c-8252-b588ad8c2981.png)
6. First step is to clone this repo content. In our case, we made ```cd /opt/model-autocompletion-server``` and cloned the repo in that folder. 
7. You may not have the glove.6B.300d.txt file inside the folder where this repo was cloned. You need to run:
``` 
    sudo wget https://issicloud.dsic.upv.es/index.php/s/HRGspSGJ0IhWN0A/download
    sudo mv download general.zip
    sudo unzip general.zip
 ```
and move the file glove.6B.300d.txt to the repo folder. 
8. It is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/opt/model-autocompletion-server/files/'

### Usage (remote mode)

If you already did the steps mentioned in the previous section, follow these ones:
1. Open PuTTY SSH Client.
2. Create a new SSH session introducing the host name and the port. In this example we have used as host name and port the following ones:
![Host name and port](https://user-images.githubusercontent.com/50658372/144410647-3a426339-384f-40e0-ab61-6ca9ff54e7e2.png)
3. Click Open. 
4. You will be required to enter a password. Write it and press Enter.
![Login](https://user-images.githubusercontent.com/50658372/144417130-1388ef74-bdd3-43fa-8fc6-77f96971967b.png)
5. Now it will appear a basic CLI.
![Console](https://user-images.githubusercontent.com/50658372/144417183-25df1659-1a31-412c-8252-b588ad8c2981.png)
6. First step is to update your files with this repo content. In our case, we made ```cd /opt/model-autocompletion-server``` and executed ```sudo git pull```. 
7. You may not have the glove.6B.300d.txt file inside the folder where this repo was cloned. You need to run:
``` 
    sudo wget https://issicloud.dsic.upv.es/index.php/s/HRGspSGJ0IhWN0A/download
    sudo mv download general.zip
    sudo unzip general.zip
 ```
and move the file glove.6B.300d.txt to the repo folder. 
8. Before running the service, it is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/opt/model-autocompletion-server/files/'
9. Now it's time to run the service. To do so, we type the command ``` sudo systemctl start model-autocompletion.service ```
10. The service may take a while to start working (1 minute max in our case). You can get to know the service status using the command ``` sudo systemctl status model-autocompletion.service ```
11. After it starts, it is possible to make queries in your browser. An example query would be: https://som-research.uoc.edu/model-autocompletion/general/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hola/7/1 
12. To stop the running service the right command is ``` sudo systemctl stop model-autocompletion.service ```
In case you want to restart it, execute the command ``` sudo systemctl restart model-autocompletion.service ```
13. Finally, to close the SSH session, execute ```exit``` and it will shut down the console. 
 
## Developer guide

### Requirements

- You need to install Docker (version 20.10.7) on your computer. Ubuntu users follow this tutorial (steps 1-6): https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04 / Windows users follow this tutorial. Windows 10 Home users should install Docker Desktop as  mentioned in this video: https://www.youtube.com/watch?v=5nX8U8Fz5S0. In case Windows 10 Home users experience some WSL errors, please check this page: https://docs.docker.com/desktop/windows/wsl/ in the prerequisites section the second point explains how to solve WSL errors.
- Download GloVe's general embeddings dictionary from the official site: https://nlp.stanford.edu/projects/glove/ We use Wikipedia 2014 + Gigaword 5 (6B tokens, 400K vocab, uncased, 50d, 100d, 200d, & 300d vectors, 822 MB download), file name: ```glove.6B.zip```. Unzip the folder and copy the file ```glove.6B.300d.txt``` to the folder where this repository will be cloned.

### Installing

Before starting this tutorial, make sure to have installed the software mentioned in the requirements section.

If it's your first time using our repository, follow these steps:
Before starting, Windows users should run Docker Desktop first. 
1. Clone our repository.
2. Open a command-line interpreter and navigate to the folder where this repository is located.
3. Before running the container and the server, it is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/files/'
4. Execute the command: ```docker build -t imageName .``` assign a name to the image that will be executed, for example, model-autocompletion. This command will run the content stored in Dockerfile. If it appears ```permissions denied```, execute: ```sudo chmod 666 /var/run/docker.sock```.
5.  Now, if you are running Docker on Linux as your host system, execute: ```docker run -it imageName```. Otherwise, if your host OS is Windows, execute: ```docker run -p 8080:8080 -it imageName```. This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 
6.  To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
7.  To make queries to the local server, open your browser and write the URL that appears inside the command-line interpreter: ![URL server](https://user-images.githubusercontent.com/50658372/127834030-dea9ed89-3651-4a9a-bad1-c25dd88589ae.png) Using the URL in the example, the query will have this structure: ```http://172.17.0.2:8080/model-autocompletion/<model>/<positive_concepts>/<negative_concepts>/<number>/<together>``` Windows users don't have to use the IP shown in the screenshot. Instead, you must write ```localhost```.
  - ```<model>```: you must specify from which model you want our suggestions. Possible values: ```general``` if you want suggestions from the general knowledge, ```contextual``` if you want suggestions from the contextual knowledge, ```general;contextual``` if you want suggestions from both sources of knowledge.
  - ```<positive_concepts>```: here you put the model's slices using the format: slice1term1,slice1term2,slice1term3;slice2term1,slice2term2;slice3term1
  - ```<negative_concepts>```: here you put the historical data (words discarded by the user) using the format: word1,word2,word3...
  - ```<number>```: you specify the number of suggestions you want.
  - ```<together>```: in case you want suggestions from both sources of knowledge, you have to specify here if you want to see the suggestions together or not. Possible values: ```1``` to see the suggestions together, ```0``` to see the suggestions provided by each source of knowledge.
  Example query (Linux users): http://172.17.0.2:8080/model-autocompletion/general/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Example query (Windows users): http://localhost:8080/model-autocompletion/general/Supervisor;Order,subordinate,create,assigned,history,status;Worker,name/hello,bye,nice/10/0
  Result: ![Result](https://user-images.githubusercontent.com/50658372/144405246-2aa19023-8ba6-4afc-94ad-dc204ffdb150.png)
7. To go out of the internal command-line interpreter type: ```exit```
8. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 

### Usage  
  If you already did the steps mentioned in the previous section, follow these ones:
 1. If you modified files stored in your local repository, copy them to the container you created before. To do that, execute: ```docker start containerName``` this command will change the container's current status to Up. 
 2. To copy the files to the container: ```docker cp fileName.extension containerID:/fileName.extension```. If you want to know your container's ID, execute the command ```docker ps -a```. This will list your containers and the relevant information like the container ID, name, status...
 3. Before running the container and the server, it is important that you check if in flaskserver.py the UPLOAD_FOLDER variable equals '/files/'
 4. Now, it's time to run again your container. This time you have to use: ```docker exec -it containerID /bin/bash``` This command will open an internal command-line interpreter for Ubuntu 20.04 (specified in Dockerfile). 
 5. To start the Flask server, in the internal command-line interpreter type: ```python3 flaskserver.py```
 6. To make queries do the same as explained in step 6 above.
 7. To go out of the internal command-line interpreter type: ```exit```
 8. If you want to stop the container's execution: ```docker stop containerID``` This command changes the execution of the current container and changes its status from Up to Exited. 


## Citations

[1] Loli Burgueño, Robert Clarisó, Sébastien Gérard, Shuai Li, Jordi Cabot: An NLP-Based Architecture for the Autocompletion of Partial Domain Models. CAiSE 2021: 91-106. Preprint: https://hal.archives-ouvertes.fr/hal-03010872/document
