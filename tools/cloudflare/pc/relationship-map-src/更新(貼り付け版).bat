@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 貼り付け.txt の内容を取り込んで、相関図の部屋を作り直します...
if not exist "貼り付け.txt" (
  python paste_ranking.py
  pause
  exit /b 1
)
python paste_ranking.py
if errorlevel 1 (
  echo.
  echo 取り込みに失敗しました。上の表示を確認してください。
  pause
  exit /b 1
)
python refresh.py --no-fetch
if errorlevel 1 (
  echo.
  echo ビルドに失敗しました。
  pause
  exit /b 1
)
echo.
echo 完了しました。ブラウザで開きます。
start "" "C:\Users\yumat\.claude\output\relationship-maps.html"
pause
