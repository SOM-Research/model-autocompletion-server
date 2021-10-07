FROM ubuntu:20.04
ADD recommender.py .
ADD flaskserver.py .
ADD slices.py .
ADD lemmatizer.py .
ADD glove.6B.300d.txt .
RUN apt-get update && apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install numpy
RUN pip install scipy
RUN pip install nltk
RUN pip install flask
RUN apt get update
RUN apt install git
RUN apt install make
RUN apt-get install gcc
RUN apt install g++-10
RUN apt install gcc-10
RUN apt-get install curl
RUN apt-get install unzip
RUN mkdir files
