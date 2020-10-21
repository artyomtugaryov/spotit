#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"

VENV_PATH+="${ROOT_DIR}/.venv"
REQUIREMENTS_FILE_PATH+="${ROOT_DIR}/requirements.txt"

python3 -m virtualenv -p `which python3` ${VENV_PATH}

source ${VENV_PATH}/bin/activate

pip install -r ${REQUIREMENTS_FILE_PATH}