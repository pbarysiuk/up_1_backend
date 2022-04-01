#!/bin/bash

####################
###   Binaries   ###
####################
DOCKER_COMPOSE=$(which docker-compose)
####################

PROJECT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

export USER_ID=${UID}
export GROUP_ID=${UID}

if [ ! -f ${PROJECT_PATH}/.env ]; then
  echo -e "No .env file present.\nCopying .env.example to .env"
  cp ${PROJECT_PATH}/.env.example ${PROJECT_PATH}/.env
fi

while read line; do export "$line";
done < <(cat ${PROJECT_PATH}/.env | grep -v "#" | grep -v "^$")

${DOCKER_COMPOSE} -f ${PROJECT_PATH}/docker-compose.yml down --remove-orphans

if [ "${REBUILD_IMAGE}" = true ]; then
    ${DOCKER_COMPOSE} -f ${PROJECT_PATH}/docker-compose.yml build --no-cache
fi

${DOCKER_COMPOSE} -f ${PROJECT_PATH}/docker-compose.yml up -d

sleep 30;

${DOCKER_COMPOSE} -f ${PROJECT_PATH}/docker-compose.yml logs -f
