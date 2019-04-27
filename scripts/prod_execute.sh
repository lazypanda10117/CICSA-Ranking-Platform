#!/usr/bin/env bash
APP_NAME=$@
if [[ -f .env ]];
then
    DATABASE_URL=$(grep DATABASE_URL .env | cut -d '=' -f 2-)
    if [[ ! -z "${DATABASE_URL// }"  ]];
    then
        export DATABASE_URL="${DATABASE_URL// }"
    else
        DB_HOST=$(grep DB_HOST .env | cut -d '=' -f 2-)
        DB_PORT=$(grep DB_PORT .env | cut -d '=' -f 2-)
        DB_NAME=$(grep DB_NAME .env | cut -d '=' -f 2-)
        DB_USER=$(grep DB_USER .env | cut -d '=' -f 2-)
        DB_PASS=$(grep DB_PAS .env | cut -d '=' -f 2-)
        if [[ ! -z "${DB_HOST// }" ]] && [[ ! -z "${DB_PORT// }" ]] && [[ ! -z "${DB_NAME// }" ]] && [[ ! -z "${DB_USER// }" ]] && [[ ! -z "${DB_PASS// }" ]];
        then
            export DB_HOST="${DB_HOST// }"
            export DB_PORT="${DB_PORT// }"
            export DB_NAME="${DB_NAME// }"
            export DB_USER="${DB_USER// }"
            export DB_PASS="${DB_PASS// }"
        fi
    fi
    BUILD_TYPE=$(grep BUILD_TYPE .env | cut -d '=' -f 2-)
    if [[ ! -z "${BUILD_TYPE// }"  ]];
    then
        export BUILD_TYPE="${BUILD_TYPE// }"
    fi
    DEBUG_MODE=$(grep DEBUG_MODE .env | cut -d '=' -f 2-)
    DJANGO_SECRET_KEY=$(grep DEBUG_MODE .env | cut -d '=' -f 2-)
    if [[ ! -z "${DEBUG_MODE// }"  ]] && [[ ! -z "${DJANGO_SECRET_KEY// }" ]];
    then
        export DEBUG_MODE="${DEBUG_MODE// }"
        export DJANGO_SECRET_KEY="${DJANGO_SECRET_KEY// }"
    fi
fi
gunicorn ${APP_NAME}.wsgi
