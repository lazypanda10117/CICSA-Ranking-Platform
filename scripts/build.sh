#!/usr/bin/env bash
if [[ -f .env ]];
then
    BUILD_TYPE=$(grep BUILD_TYPE .env | cut -d '=' -f 2-)
    BUILD_LOC=$(grep BUILD_LOC .env | cut -d '=' -f 2-)
    BUILD_TYPE="${BUILD_TYPE// }"
    BUILD_LOC="${BUILD_LOC// }"

    if [[ ! -z "${BUILD_TYPE}" ]] && [[ ! -z "${BUILD_LOC}" ]];
    then
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
    fi
fi
