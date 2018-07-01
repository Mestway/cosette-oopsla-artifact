FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y software-properties-common

RUN add-apt-repository ppa:plt/racket
RUN apt-get update && \
    apt-get install -y racket && \
    apt-get install -y python2.7 python-pip

RUN raco pkg install rosette

RUN apt-get install -y python3-pip python3-dev \
        && cd /usr/local/bin \
        && ln -s /usr/bin/python3 python \
        && pip3 install --upgrade pip