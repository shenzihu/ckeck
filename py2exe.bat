@echo off
cd ..
set path_root=%CD%
python %CD%\check\setup.py py2exe -d %path_root%\target
rd build /s /q

pause
