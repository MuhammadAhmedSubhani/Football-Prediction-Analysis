# FIFA World Cup 2026 Analytics — Web Frontend

This folder adds a Streamlit frontend to the supplied `Football Prediction Analysis.py`
and connects it to the supplied `world-cup-2026-team-schedules.csv`.

## Run locally

```bash
cd world_cup_2026_frontend
python -m pip install -r requirements.txt
streamlit run app.py
```

Then open the local address shown by Streamlit (normally http://localhost:8501).

## What is connected

- Team selector/search
- FIFA rating data from the original Python class
- Original telemetry generator for passes and shots/xG
- Original Monte Carlo win/draw/loss simulation
- Uploaded World Cup schedule CSV
- Match and live-score links contained in the CSV
- Interactive Plotly pitch/shot/pass charts

The original analytics file is copied into this folder as
`football_prediction_analysis.py` so the frontend can import it cleanly.
