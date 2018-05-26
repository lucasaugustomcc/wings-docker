#!/bin/bash

checkExitCode() {
if [ $? -ne 0 ]; then
    echo "Error"
    exit 1;
fi
}

BASEDIR=`dirname $0`

. $BASEDIR/io.sh 3 1 1 "$@"

$BASEDIR/generic_code $INPUTS1 $INPUTS2 $INPUTS3 $PARAMS1 $OUTPUTS1

checkExitCode
Lucas