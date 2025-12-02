@echo off
title Tool Tuyen Dung Bell System24
color 0A

echo ==================================================
echo      DANG KHOI DONG HE THONG TUYEN DUNG
echo ==================================================
echo.

:: 1. Kiem tra xem co Python chua
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [LOI NGHIEM TRONG] May tinh chua cai Python hoac chua cai dung cach!
    echo.
    echo Vui long:
    echo 1. Go bo ban Python hien tai.
    echo 2. Tai Python 3.11 (Link da gui).
    echo 3. Nho tich vao o "Add Python to PATH" khi cai dat.
    echo.
    pause
    exit
)

echo [1/3] Dang nang cap he thong cai dat (pip)...
python -m pip install --upgrade pip

echo.
echo [2/3] Dang cai dat thu vien can thiet...
:: Lenh nay se cai dat ma khong can build lai tu dau (tranh loi cmake)
python -m pip install -r requirements.txt --only-binary=:all:

echo.
echo [3/3] Dang mo trinh duyet...
echo --------------------------------------------------
echo LUU Y: Hay giu cua so den nay luon mo nhe!
echo --------------------------------------------------
echo.

:: Chay tool qua module python de tranh loi not recognized
python -m streamlit run app_job.py

pause