#!/bin/bash 
time docker run -it --rm -v "$PWD":/home/crisprlab -e "CL_UID=$UID" crisprlab/crisprdisco disco $@
