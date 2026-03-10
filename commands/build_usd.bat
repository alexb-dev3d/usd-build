@echo off

rem these env variables can be overriden at will
rem set DOWNLOAD_DIR=dependencies
rem set BUILD_DIR=build

rem usage:
rem build_usd.bat configs\open_usd.25.08.json ..\3rd_parties\OpenUsd-25.05
python packages\build_it.py %1 %2