#!/bin/bash
# This script installs python dependencies listed in requirements.txt
python3 -m pip uninstall serial pyserial -y
python3 -m pip install -r ../../scale_UI/requirements.txt