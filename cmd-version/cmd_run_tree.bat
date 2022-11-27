@echo off
chcp 1255
FOR /d %%i in ("J:\שמע\כל המוזיקה\*") do call "%~dp0\Duplicatedetectiontree.bat" "%%~i" && cd "J:\שמע\כל המוזיקה"

pause