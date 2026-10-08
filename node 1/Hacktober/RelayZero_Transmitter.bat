@echo off
echo Starting RelayZero Base Station...
cd "C:\Users\chaga\OneDrive\Desktop\Hacktober"

:: Launch Chrome as a native app window
start chrome --app=http://localhost:8501

:: Start Streamlit quietly in the background
streamlit run base_station.py --server.headless true