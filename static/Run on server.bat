@echo off
call conda activate FaceRecogNN
set FLASK_APP=app.py
start /min cmd /k "flask run & ping 127.0.0.1 -n 2 > nul"
start /min cmd /c "ngrok http 5000"
start http://127.0.0.1:4040
timeout /t 2 > nul
powershell -Command "& {$response = Invoke-WebRequest -Uri 'http://127.0.0.1:4040/api/tunnels' -Headers @{'ngrok-skip-browser-warning'='true'}; Write-Output $response.Content}"
