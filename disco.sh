#!/bin/bash
time docker run -it --rm -v "$PWD":"$PWD" -v "$PWD":/home/crisprlab -w "$PWD" -e UID=$UID --user $UID crisprlab/crisprdisco disco $@
