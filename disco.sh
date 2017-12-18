#!/bin/bash 
time docker run -it --rm -v "/mnt":"/mnt" -v "$PWD":/home/crisprlab -v "test":"/opt/app/test" -e "CL_UID=$UID" crisprlab/crisprdisco disco $@
