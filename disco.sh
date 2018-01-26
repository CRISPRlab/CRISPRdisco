#!/bin/bash 
time docker run -it --rm -v "$PWD":/home/crisprlab -e UID=$UID -e GID=$GID --user $UID crisprlab/crisprdisco disco $@
