@echo off
TITLE CHECK LOI TUYEN DUNG TOOL
color 0F

echo ==================================================
echo      DANG KIEM TRA LOI (DEBUG MODE)
echo ==================================================
echo.

:: 1. Kiem tra lenh python
echo [Buoc 1] Kiem tra Python...
python --version
IF %ERRORLEVEL% NEQ 0 (
    goto :LOI_PYTHON
)

:: 2. Cai dat thu vien
echo.
echo [Buoc 2] Cai dat thu vien...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [CANH BAO] Co loi khi cai dat thu vien. 
    echo Hay chup anh man hinh gui cho Admin neu Tool khong chay.
    echo.
)

:: 3. Chay Tool
echo.
echo [Buoc 3] Khoi dong Web App...
python -m streamlit run app_job.py

:: QUAN TRONG: Lenh nay giu man hinh khong bao gio tat
pause
exit

:LOI_PYTHON
color 0C
echo.
echo ==================================================
echo [LOI NGHIEM TRONG] MAY TINH CHUA TIM THAY PYTHON!
echo ==================================================
echo.
echo Nguyen nhan co the la:
echo 1. Ban chua cai Python.
echo 2. Ban da cai nhung QUEN tich vao o "Add Python to PATH".
echo.
echo Cach sua:
echo - Go cai dat Python hien tai.
echo - Cai lai Python va nho tich vao o vuong "Add Python to PATH" o man hinh dau tien.
echo.
pause