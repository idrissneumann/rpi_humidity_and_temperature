#!/bin/bash

BASE_DIR="$(dirname $0)"
REPO_PATH="${BASE_DIR}/.."
IMAGE="veggiepi-${1}"
VERSION="${2}"
ARCH="arm"

tag_and_push() {
  docker tag "comworkio/${2}:latest" "comworkio/${2}:latest-${3}" 
  docker tag "comworkio/${2}:latest" "comworkio/${2}:${1}-${3}"
  docker push "comworkio/${2}:${1}-${3}"
  docker push "comworkio/${2}:latest"
}

cd "${REPO_PATH}" && git pull origin main || : 
git config --global user.email "${GIT_EMAIL}"
git config --global user.name "${GIT_EMAIL}"
sha="$(git rev-parse --short HEAD)"
echo '{"version":"'"${VERSION}"'", "sha":"'"${sha}"'", "arch":"'"${ARCH}"'"}' > manifest.json

COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build --no-cache "${IMAGE}"

echo "${DOCKER_ACCESS_TOKEN}" | docker login --username comworkio --password-stdin

tag_and_push "${VERSION}" "${IMAGE}" "${ARCH}"
tag_and_push "${VERSION}-${CI_COMMIT_SHORT_SHA}" "${IMAGE}" "${ARCH}"

git add .
git stash
git stash clear
