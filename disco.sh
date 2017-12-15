#!/bin/bash 
time docker run -it --rm -v "/mnt":"/mnt" -v "$PWD":/home/crisprlab -e "CL_UID=$UID" crisprlab/crisprdisco disco $@
