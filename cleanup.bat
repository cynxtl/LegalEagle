@echo off
REM Cleanup script for LegalEagle v2
REM This removes backend integration files and documentation

cd /d "c:\Users\ASUS VIVOBOOK 15 S\Desktop\Law.ai"

REM Delete documentation files created
del API_RESPONSE_FORMAT.md 2>nul
del CHANGES_SUMMARY.md 2>nul
del DOCUMENTATION_INDEX.md 2>nul
del FRONTEND_BACKEND_INTEGRATION.md 2>nul
del FRONTEND_README.md 2>nul
del IMPLEMENTATION_COMPLETE.md 2>nul
del SETUP_GUIDE.md 2>nul
del START_HERE.md 2>nul
del VERIFICATION_CHECKLIST.md 2>nul
del VISUAL_SUMMARY.md 2>nul

REM Delete .env.example from frontend
del frontend\.env.example 2>nul

REM Delete api-client.ts from frontend
del frontend\lib\api-client.ts 2>nul

REM Delete start-dev.bat from frontend
del frontend\start-dev.bat 2>nul

echo Cleanup complete!
echo Now run: git add -A && git commit -m "Remove backend integration, hide scrollbars, clean repo"
pause
