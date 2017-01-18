#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/.."

# Let Django figure out what release this is
./scripts/echo_version_json.sh > ./hostedfactor/version.json

docker build -f Dockerfile -t  . || exit 1
