FROM ubuntu:20.04
ADD recommender.py .
ADD serverflask.py .
ADD slices.py .
ADD vectors_emasa_en.txt . 
ADD general.txt .
RUN apt-get update && apt-get install --no-install-recommends -y python3.8 python3-pip python3.8-dev
RUN pip install numpy
RUN pip install scipy
RUN pip install nltk
RUN pip install flask
