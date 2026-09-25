@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1

where py.exe >nul 2>&1
if %errorlevel%==0 (
  py.exe -3 -m pip install --upgrade pyinstaller
  py.exe -3 -m PyInstaller --noconfirm --clean --onefile --windowed --name ScrcpyQuickLaunch app.py
  goto :done
)

where python.exe >nul 2>&1
if %errorlevel%==0 (
  python.exe -m pip install --upgrade pyinstaller
  python.exe -m PyInstaller --noconfirm --clean --onefile --windowed --name ScrcpyQuickLaunch app.py
  goto :done
)

echo Python 3 was not found.
pause
exit /b 1

:done
echo.
echo Build finished. Check the dist folder.
pause
