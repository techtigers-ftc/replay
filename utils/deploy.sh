#!/bin/bash
SCRIPT_DIR=$(dirname ${BASH_SOURCE[0]})
source ${SCRIPT_DIR}/settings.env
source ${SCRIPT_DIR}/styles.env

TARGET=${1}
CONNECTION_TYPE=${2}
BUILD_DIR=./build

if [ "${TARGET}" == "core" ]
then
    TARGET_NAME='techtigers library'
    SOURCE_DIR=${SCRIPT_DIR}/../techtigers
    COMPILED_FILE=${BUILD_DIR}/techtigers.mpy
    SINGLE_SOURCE=${BUILD_DIR}/techtigers.py
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
elif [ "${TARGET}" == "mission" ]
then
    TARGET_NAME='missions'
    SOURCE_DIR=${SCRIPT_DIR}/../missions
    COMPILED_FILE=${BUILD_DIR}/missions.mpy
    SINGLE_SOURCE=${BUILD_DIR}/missions.py
    FILES=(
        missions.py
    )
else
    print "${COL_RED}Error! Invalid target ${COL_YELLOW}[${TARGET}]"
    print "Must be ${COL_YELLOW}core${COL_NORMAL} or ${COL_YELLOW}mission."
    exit 1
fi

if [ "${CONNECTION_TYPE}" == "wire" ]
then
    PORT=${WIRED_PORT}
else
    PORT=${BLE_PORT}
fi

show_banner

print "Building ${COL_ORANGE}${TARGET_NAME}"

print "Going to use port: ${COL_CYAN}${PORT}"

export PATH=${PATH}:~/Library/Python/${PYTHON_VERSION}/lib/python/site-packages/mpy_cross

print "Creating Build directory: ${COL_CYAN}${BUILD_DIR}"
mkdir -p ${BUILD_DIR}

print "Creating single source file: ${COL_CYAN}${SINGLE_SOURCE}"
grep --no-filename import ${SOURCE_DIR}/*.py | grep -vE '\s\.' | uniq > ${SINGLE_SOURCE}

print "Appending source code to single file: ${COL_CYAN}${SINGLE_SOURCE}"
for file in ${FILES[*]}
do
    cat ${SOURCE_DIR}/${file} | grep -vE '^.*import.*' >> ${SINGLE_SOURCE}
done

print "Compiling single file: ${COL_CYAN}${SINGLE_SOURCE} --> ${COL_LIGHT_GREEN}${COMPILED_FILE}"
mpy-cross -o ${COMPILED_FILE} ${SINGLE_SOURCE} || exit 

print "Ampy put the Compiled File: ${COL_LIGHT_GREEN}${COMPILED_FILE}"
ampy -p ${PORT} put ${COMPILED_FILE}
ampy -p ${PORT} reset

print "Removing Build directory: ${COL_CYAN}${BUILD_DIR}${COLOR_NORMAL}"
rm -rf ${BUILD_DIR}

print "Done :)"
