@echo off
:: This script installs python dependencies listed in requirements.txt
python -m pip uninstall serial pyserial -y
python -m pip install -r ../../scale_UI/requirements.txt
