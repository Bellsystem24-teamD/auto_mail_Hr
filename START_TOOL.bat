@echo off
title Tool Tuyen Dung Bell System24
color 0A

echo ==================================================
echo      DANG KHOI DONG HE THONG TUYEN DUNG
echo ==================================================
echo.

:: Kiem tra xem may da cai Python chua
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [LOI] May tinh chua cai Python!
    echo Vui long tai va cai dat Python tai: python.org
    echo Nho tich vao o "Add Python to PATH" khi cai dat.
    pause
    exit
)

echo [1/2] Dang kiem tra va cai dat thu vien (Vui long doi)...
:: Bo lenh giau loi de neu co loi mang thi con biet
python -m pip install -r requirements.txt

echo.
echo [2/2] Dang mo trinh duyet...
echo Hay giu cua so nay luon mo nhe!
echo.

:: DUNG LENH NAY SE CHAY ON DINH HON
python -m streamlit run app_job.py

pause