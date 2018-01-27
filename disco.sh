#!/bin/bash
time docker run -it --rm -v "$PWD":/home/crisprlab -e UID=$UID --user $UID -e CL_UID=$UID crisprlab/crisprdisco disco $@
