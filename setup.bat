@echo off
REM Automated Database Setup for Employee Vacation System
REM This script will help you set up the database tables

echo ========================================
echo Employee Vacation Management System
echo Database Setup Script
echo ========================================
echo.

echo [Step 1] Installing Python dependencies...
pip install -q supabase bcrypt

echo.
echo [Step 2] Running database setup verification...
python setup_database.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Go to your Supabase dashboard
echo 2. Execute the SQL schema as instructed above
echo 3. Run: streamlit run app.py
echo.
pause
