@echo off
cd /d "%~dp0"
echo CattleChain start ho raha hai... Browser mein http://localhost:8501 khulega.
echo Is window ko BAND NA karein, warna app band ho jayegi.
venv\Scripts\python -m streamlit run app.py
pause
