@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 日経のランキングを取得して、相関図の部屋を作り直します...
python refresh.py
if errorlevel 1 (
  echo.
  echo 失敗しました。上の表示を確認してください。
  pause
  exit /b 1
)
echo.
echo 完了しました。ブラウザで開きます。
start "" "C:\Users\yumat\.claude\output\relationship-maps.html"
pause
