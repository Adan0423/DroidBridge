@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

rem Usar pythonw para no dejar consola abierta
where pyw.exe >nul 2>&1
if %errorlevel%==0 (
  start "" pyw.exe -3 "%~dp0main.py"
  exit /b 0
)

where pythonw.exe >nul 2>&1
if %errorlevel%==0 (
  start "" pythonw.exe "%~dp0main.py"
  exit /b 0
)

rem Fallback con consola visible
where py.exe >nul 2>&1
if %errorlevel%==0 (
  py.exe -3 "%~dp0main.py"
  exit /b
)

where python.exe >nul 2>&1
if %errorlevel%==0 (
  python.exe "%~dp0main.py"
  exit /b
)

echo Python 3 no encontrado.
echo Instala Python 3 y agregalo al PATH.
pause
exit /b 1
