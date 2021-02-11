#!/bin/bash

REPO_PATH="/home/centos/humidity_and_temperature/"

cd "${REPO_PATH}" && git pull origin main || :
git push github main
git push pgitlab main
exit 0
