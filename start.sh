#!/bin/bash
# Based on Jupyter docker stacks model

if [ $UID == 0 ] ; then
    if [ "$CL_UID" != $(id -u $CL_USER) ] ; then
        usermod -u $CL_UID $CL_USER
        chown -R $CL_UID $CONDA_DIR
    fi

    exec su $CL_USER -c "env PATH=$PATH $*"
else
    exec $*
fi
