#! /usr/bin/env sh
export PYTHONPATH="src/edeposit:$PYTHONPATH"

py.test tests $@