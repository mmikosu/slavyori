:Start
@echo off
color 0b
title Slavyori Discord Bot
echo Starting Slavyori
python index.py
echo.
echo -------------------------------------------------------------
echo (%time%) [WARNING]: Slavyori closed or crashed, restarting!
echo -------------------------------------------------------------
goto Start
