FROM ubuntu:20.04
ADD demo.sh . 
ADD recommender.py .
ADD flaskserver.py .
ADD mongoDB.py .
ADD lemmatizer.py .
ADD requirements.txt .
RUN apt-get update && apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y gcc
RUN apt-get install -y make
RUN mkdir -p opt/model-autocompletion-server/files/
ADD glove.6B.300d.txt opt/model-autocompletion-server/files/
ADD emasa.txt opt/model-autocompletion-server/files/
