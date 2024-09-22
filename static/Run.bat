@echo off
call conda activate FaceRecogNN
set FLASK_APP=app.py
start cmd /k "flask run & ping 127.0.0.1 -n 2 > nul"
start http://127.0.0.1:5000/
