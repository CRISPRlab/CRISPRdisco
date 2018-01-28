#!/bin/bash
time docker run -it --rm -v "$PWD":"$PWD" -v "$PWD":/home/crisprlab -m "$PWD" -e UID=$UID --user $UID -e CL_UID=$UID crisprlab/crisprdisco disco $@
