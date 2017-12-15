#!/bin/bash

# http://unix.stackexchange.com/questions/55913/whats-the-easiest-way-to-find-an-unused-local-port
while :
do
        PORT="`shuf -i 8888-9999 -n 1`"
        ss -lpn | grep -q ":$PORT " || break
done
export PORT

export NAME=$USER\_crisprdisco_jupyter
export HOST=$(hostname -f)

docker run \
    -it \
    --rm \
    -v "/mnt":"/mnt" \
    -v "$PWD":"$PWD" \
    -w "$PWD" \
    -p $PORT:$PORT \
    -e "NB_UID=$UID" \
    -e "GRANT_SUDO=yes" \
    --name $NAME \
    --user root --group-add users crisprlab/crisprdisco_jupyter start-notebook.sh --port $PORT --NotebookApp.base_url=$NAME 2>&1 | sed "s/localhost/${HOST}/g"

