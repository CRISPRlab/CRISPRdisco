#!/bin/bash

# http://unix.stackexchange.com/questions/55913/whats-the-easiest-way-to-find-an-unused-local-port
while :
do
        PORT="`shuf -i 8888-9999 -n 1`"
        ss -lpn | grep -q ":$PORT " || break
done
export PORT

while :
do
        DB_PORT="`shuf -i 3000-3999 -n 1`"
        ss -lpn | grep -q ":$DB_PORT " || break
done

NAME="crawler_notebook"

while getopts 'p:n:' opt
    do
        case $opt in
            p) DB_PORT=$OPTARG;;
            n) NAME=$OPTARG;;
        esac
done
export DB_PORT
export NAME

export HOST=$(hostname)

export NB_UID=$UID

export DOCKER_CLIENT_TIMEOUT=120
export COMPOSE_HTTP_TIMEOUT=120

docker-compose up -d 2>&1 | sed "s/localhost/${HOST}/"

./get_URL.sh
