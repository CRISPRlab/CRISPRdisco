#!/bin/bash
set -ev

echo "${TRAVIS_BRANCH}"

if [ "${TRAVIS_BRANCH}" = "master" ]; then
    docker push crisprlab/crisprdisco:latest
fi
