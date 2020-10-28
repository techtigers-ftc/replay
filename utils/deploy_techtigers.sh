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

COMPILED_FILE=techtigers.mpy
SINGLE_SOURCE=techtigers.py
SOURCE_DIR=../techtigers
FILES=(
    timer.py
    color_matcher.py
    reflected_light_matcher.py
    line_edge.py
    line_sensor.py
    logger.py
    test_case.py
    test_runner.py
    colors.py
    pid.py
    robot.py
)

echo "Creating single source file: ${SINGLE_SOURCE}"
grep -i --no-filename import ${SOURCE_DIR}/*.py | grep -vE '\s\.' | uniq > ${SINGLE_SOURCE}

echo "Appending source code to single file: ${SINGLE_SOURCE}"
for file in ${FILES[*]}
do
    cat ${SOURCE_DIR}/${file} | grep -vE '^.*import.*' >> ${SINGLE_SOURCE}
done

echo "Compiling single file: ${SINGLE_SOURCE} --> Compiled File: ${COMPILED_FILE}"
mpy-cross techtigers.py

echo "Ampy put the Compiled File: ${COMPILED_FILE}"
ampy -p ${PORT} put ${COMPILED_FILE}
ampy -p ${PORT} reset
# ampy -p ls /dev/tty* | grep -i usbmodem reset

echo "Removing Files"
rm -f ${SINGLE_SOURCE}
rm -f ${COMPILED_FILE}

echo "Done :)"
