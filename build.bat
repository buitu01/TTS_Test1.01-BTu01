@echo off
echo Dang dong goi ung dung Text-to-Speech...
echo.
pyinstaller --noconfirm --onedir --windowed --name "TextToSpeech_Vi" main.py
echo.
echo Dong goi hoan tat! Kiem tra thu muc 'dist/TextToSpeech_Vi'.
pause
