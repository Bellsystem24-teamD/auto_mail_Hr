@echo off
title Tool Tuyen Dung Bell System24
color 0A

echo ==================================================
echo      DANG KHOI DONG HE THONG TUYEN DUNG
echo ==================================================
echo.

echo [1/2] Dang kiem tra va cai dat thu vien...
pip install -r requirements.txt >nul 2>&1

echo [2/2] Dang mo trinh duyet...
echo.
echo Hay giu cua so nay mo trong khi su dung Tool nhe!
echo.

streamlit run app_job.py

pause