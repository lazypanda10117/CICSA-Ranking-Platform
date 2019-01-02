#!/usr/bin/env bash
BUILD_TYPE=$(python3 ./scripts/build.py 1)
BUILD_LOC=$(python3 ./scripts/build.py 2)

echo "Build Type: ${BUILD_TYPE} "
echo "Building In ${BUILD_TYPE} Mode On ${BUILD_LOC}"

if [[ ${BUILD_TYPE} = "DEV" ]];
then
    if [[ ${BUILD_LOC} = "LOCAL" ]];
    then
        $(make dev-run)
    elif [[ ${BUILD_LOC} = "SERVER" ]];
    then
        $(make dev-run-server)
    else
        echo "Error: Unknown Build Type/Location" >&2
        exit 1;
    fi
elif [[ ${BUILD_TYPE} = "PROD" ]];
then
    $(make prod-run)
else
    echo "Error: Unknown Build Type/Location" >&2
    exit 1;
fi
