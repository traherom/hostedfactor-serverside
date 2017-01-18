#!/bin/sh
cat >docker-compose.ci.yml <<EOF
version: '2'
services:
  web:
    image: $CONTAINER_TEST_IMAGE
    environment:
      - CI
EOF
