#! /usr/bin/env sh
export PYTHONPATH="src/edeposit/amqp/:$PYTHONPATH"

py.test tests $@