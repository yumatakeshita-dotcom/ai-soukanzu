@echo off
rem 相関図の公開(Claude不要)。ビルド → 公開フォルダ作成 → Cloudflareへ反映
cd /d "%~dp0"
python -I refresh.py --no-fetch || goto :fail
python -I publish_static.py || goto :fail
cd /d "%~dp0..\relationship-map-site"
call npx wrangler deploy -c ..\relationship-map-static\wrangler.toml || goto :fail
echo.
echo 完了しました。
pause
exit /b 0
:fail
echo.
echo 失敗しました。上のメッセージを確認してください。
pause
exit /b 1
