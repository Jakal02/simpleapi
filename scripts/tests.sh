#!/usr/bin/env bash

# run tests

echo "Script executed from ${PWD}"

hehe=$(basename ${PWD})

if [ "${hehe}" != "simpleapi" ]; then
    echo "Execute this script from the simpleapi directory"
    exit 1
fi

# Run pytest

pytest
