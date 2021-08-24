@echo off

if exist venv\ rmdir /s /q venv\

python -m venv venv
call venv\Scripts\activate
pip install --upgrade --disable-pip-version-check -q -r requirements.txt
deactivate
