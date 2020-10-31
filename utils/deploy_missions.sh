#!/bin/bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
source ${SCRIPT_DIR}/settings.env
source ${SCRIPT_DIR}/styles.env

CONNECTION_TYPE=${1}

if [ "${CONNECTION_TYPE}" == "ble" ]
then
    PORT=${BLE_PORT}
else
    PORT=${WIRED_PORT}
fi

show_banner

print "Putting ${COL_ORANGE}Mission${COL_NORMAL} code"

print "Going to use port: ${COL_CYAN}${PORT}"

export PATH=${PATH}:~/Library/Python/${PYTHON_VERSION}/lib/python/site-packages/mpy_cross

BUILD_DIR=./build
MISSIONS_FILE=./utils/missions.py
MISSIONS_SOURCE=missions_source.py
COMPILED_FILE=${BUILD_DIR}/missions_source.mpy
SINGLE_SOURCE=${BUILD_DIR}/${MISSIONS_SOURCE}

print "Creating Build directory: ${COL_CYAN}${BUILD_DIR}"
mkdir -p ${BUILD_DIR}

print "Copying and moving missions file to single source file: ${COL_PURPLE}${MISSIONS_FILE}${COL_NORMAL} --> ${COL_CYAN}${SINGLE_SOURCE}"
cp ${MISSIONS_FILE} ${MISSIONS_SOURCE}
mv ${MISSIONS_SOURCE} ${BUILD_DIR}

print "Compiling single file: ${COL_CYAN}${SINGLE_SOURCE} --> ${COL_LIGHT_GREEN}${COMPILED_FILE}"
echo ${SINGLE_SOURCE}
mpy-cross ${SINGLE_SOURCE} || exit 

print "Ampy put the Compiled File: ${COL_LIGHT_GREEN}${COMPILED_FILE}"
ampy -p ${PORT} put ${COMPILED_FILE}
ampy -p ${PORT} reset
# ampy -p ls /dev/tty* | grep -i usbmodem reset

print "Removing Build directory: ${COL_CYAN}${BUILD_DIR}${COLOR_NORMAL}"
rm -rf ${BUILD_DIR}

print "Done :)"
