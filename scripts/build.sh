#!/usr/bin/env bash
BUILD_TYPE=$(python3 ./scripts/build.py)
if [[ ${BUILD_TYPE} = "DEV" ]];
then
    echo "Build Type: ${BUILD_TYPE} "
    echo "Building In ${BUILD_TYPE} Mode"
    $(make dev-run)
elif [[ ${BUILD_TYPE} = "PROD" ]];
then
    echo "Build Type: ${BUILD_TYPE} "
    echo "Building In ${BUILD_TYPE} Mode"
    $(make prod-run)
else
    echo "Build Type: ${BUILD_TYPE} Does Not Exist. Resolving to Default Action"
    echo "Building In ${BUILD_TYPE} Mode"
    $(make prod-run)
fi
