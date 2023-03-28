@echo off
chcp 1255

echo לחיפוש לפי קוד בינארי הקש 1
echo לחיפוש לפי שם הקש 2
choice /c 12

if %errorlevel% == 2 goto :b
if %errorlevel% == 1 goto :a

:a
for /d %%i in ("J:\שמע\כל המוזיקה\*") do "%~dp0\Find_duplic_ample.py" "%%~i"
pause
exit

:b
for /d %%i in ("J:\שמע\כל המוזיקה\*") do "%~dp0\Find_duplic_names.py" "%%~i"
pause
exit