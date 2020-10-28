#!/bin/bash

CONNECTION_TYPE=${1}

if [ "${CONNECTION_TYPE}" == "ble" ]
then
    PORT=/dev/tty.LEGOHub40BD32460790-Ser
else
    PORT=/dev/tty.usbmodem3664395831381
fi

echo "Going to use port: ${PORT}"

export PATH=${PATH}:~/Library/Python/3.8/lib/python/site-packages/mpy_cross

COMPILED_FILE=missions.mpy
SINGLE_SOURCE=missions.py
SOURCE_DIR=../techtigers

echo "Compiling single file: ${SINGLE_SOURCE} --> Compiled File: ${COMPILED_FILE}"
mpy-cross ${SINGLE_SOURCE}

echo "Ampy put the Compiled File: ${COMPILED_FILE}"
ampy -p ${PORT} put ${COMPILED_FILE}
ampy -p ${PORT} reset
# ampy -p ls /dev/tty* | grep -i usbmodem reset

echo "Removing Files"
rm -f ${SINGLE_SOURCE}
rm -f ${COMPILED_FILE}

echo "Done :)"
