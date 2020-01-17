:Start
@echo off
color 0b
title Slavyori DBL API
echo Starting Slavyori DBL Counter
node --harmony dbl.js
echo.
echo -----------------------------------------------------------------------
echo (%time%) [WARNING]: DBL API Counter closed or crashed, restarting!
echo -----------------------------------------------------------------------
goto Start
