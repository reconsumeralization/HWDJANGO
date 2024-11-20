@echo off

REM Ensure we're in the project root
cd %~dp0\..

REM Create necessary directories if they don't exist
mkdir apps\hwroad apps\hwasphalt backend 2>nul

REM Move Django files to backend if they're in the root
if exist manage.py (
    move manage.py backend\
    move crm backend\
    move web_front backend\
    move templates backend\
    move static backend\
    move requirements.txt backend\
)

REM Install dependencies
echo Installing dependencies...
call npm install

REM Install Python dependencies
echo Installing Python dependencies...
cd backend
python -m venv .venv
call .venv\Scripts\activate

REM Install requirements
pip install -r requirements.txt

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Start development servers
echo Starting development servers...
cd ..
npm run dev:all
