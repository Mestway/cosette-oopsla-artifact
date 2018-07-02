FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y software-properties-common

RUN add-apt-repository ppa:plt/racket
RUN apt-get update && \
    apt-get install -y racket && \
    apt-get install -y python2.7 python-pip

RUN raco pkg install rosette

RUN apt-get update
RUN apt-get install -y software-properties-common vim unzip
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update

RUN apt-get install -y build-essential python3.6 python3.6-dev python3-pip python3.6-venv
RUN apt-get install -y git

# update pip
RUN python3.6 -m pip install pip --upgrade

RUN add-apt-repository ppa:openjdk-r/ppa  
RUN apt-get update   
RUN apt-get install -y openjdk-8-jdk  
