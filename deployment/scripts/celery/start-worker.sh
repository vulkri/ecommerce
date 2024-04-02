#!/bin/bash

set -o errexit
set -o nounset

python -m celery -A backend worker -l info