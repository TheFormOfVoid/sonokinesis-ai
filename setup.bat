@echo off
rem Runs setup.ps1 without changing the PowerShell script policy. Arguments are passed on (-Beatform path).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1" %*
pause
