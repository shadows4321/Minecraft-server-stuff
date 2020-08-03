#!/bin/bash

cd "$(dirname "$0")"
. ./settings.sh

# makes things easier if script needs debugging
if [ x$FTB_VERBOSE = xyes ]; then
    set -x
fi

check_libraries() {
    if ! command -v jq &> /dev/null
    then
        echo "jq not found. jq is required for JSON parsing"
        exit
    fi

    if ! command -v ${JAVACMD} &> /dev/null
    then
        echo "Java command \"${JAVACMD}\" not found. It is required for running the server"
        exit
    fi
    if ! command -v nc &> /dev/null
    then
        echo "Netcat command (nc) not found. It is required for checking if server port is running already"
        exit
    fi    
}

update_check() {
    check_libraries

    current_version="-1" # Default version

    if [ ! -f ${UPDATE_FILE} ]; then
        echo ${current_version} > ${UPDATE_FILE}
    else
        current_version=$(<${UPDATE_FILE})
    fi

    latest_version=`curl -JLs ${VERSION_LIST} | jq -r .build` # Gets the build key of the JSON result

    echo "USING VERSION ${current_version} WHILE LATEST IS ${latest_version}"

    if [ ! ${current_version} -eq ${latest_version} ] ; then

        echo "UPDATING TO NEW VERSION"
        curl -JLo ${JARFILE} ${DOWNLOAD_URL}

        if [ ! "$?" -eq 0 ]; then
            echo "FAILED TO DOWNLOAD LATEST VERSION OF MINECRAFT SERVER"
        fi

        echo ${latest_version} > ${UPDATE_FILE}
    fi
}

# cleaner code
eula_false() {
    grep -q 'eula=false' eula.txt
    return $?
}

# Checks if the server is already running by checking if the port is open
check_server_port() {
	 nc -z -v -w5 localhost ${MC_PORT} &> /dev/null
	 if [ "$?" -eq 0 ]; then
		echo Sever already running,stopping
		sleep 2s
		exit
	fi
}

start_server() {
	check_server_port

    update_check
    "$JAVACMD" ${JVM_ARGUMENTS}
}

# check if there is eula.txt and if it has correct content
if [ $EULA_REQUIRED = true ] ; then

    # inform user if eula.txt not found
    if [ ! -f eula.txt ]; then
       >&2 echo "Missing eula.txt. Startup will fail and eula.txt will be created"
       >&2 echo "Make sure to read eula.txt before playing!"
    fi

    if [ -f eula.txt ] && eula_false ; then
        >&2 echo "Make sure to read eula.txt before playing!"
        exit -1
    fi
fi



echo "Starting server"
start_server

