#!/bin/bash
time docker run -it --rm -v "$PWD":"$PWD" -v "$PWD":/home/crisprlab -w "$PWD" -e UID=$UID --user $UID -e CL_UID=$UID -e "GRANT_SUDO=yes" crisprlab/crisprdisco disco $@
