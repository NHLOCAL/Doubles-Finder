@echo off
chcp 1255

for /d %%i in ("J:\���\�� �������\*") do "%~dp0\Find_duplic_ample.py" "%%~i\�������"

pause