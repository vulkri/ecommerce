#!/bin/bash

set -o errexit
set -o nounset

sleep 30 # wait for backend init
python -m celery -A backend worker -l info