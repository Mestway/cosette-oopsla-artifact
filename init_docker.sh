#!/bin/bash

DIR="/cosette-artifact"
# the command to build and test solver
IMG_NAME="cosette-artifact-img"
CONTAINER_NAME="cosette-artifact"

if [[ "$(docker images -q $IMG_NAME 2> /dev/null)" == "" ]]; then
    docker build -t $IMG_NAME .
fi

echo "[0] starting container with name $NAME ..."
docker run -v $(pwd)/:$DIR -w $DIR --name=$CONTAINER_NAME -it $IMG_NAME bash