@echo off
chcp 1255
FOR /d %%i in ("J:\���\�� �������\*") do call "%~dp0\Duplicatedetectiontree.bat" "%%~i" && cd "J:\���\�� �������"

pause