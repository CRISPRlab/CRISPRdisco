#!/bin/bash

name=${1:-"crisprdisco_notebook"}
HOST=$(hostname)

URL_out=`docker exec --user jovyan -it ${name} jupyter notebook list`
URL_out=`echo "${URL_out}" | sed s/localhost/"${HOST}/"`

echo "${URL_out}"
