import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import sys

# Reuse the original analytics class supplied by the user.
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))
from football_prediction_analysis import WorldCupAnalyticsApp

st.set_page_config(
    page_title="FIFA World Cup 2026 Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.hero {
    padding: 1.5rem 1.8rem;
    border: 1px solid rgba(148,163,184,.18);
    border-radius: 22px;
    background: linear-gradient(135deg, #111827 0%, #172554 100%);
    margin-bottom: 1.25rem;
}
.hero h1 {margin: 0; font-size: 2.25rem;}
.hero p {color: #cbd5e1; margin: .5rem 0 0;}
.metric-card {
    padding: 1rem;
    border-radius: 16px;
    background: #111827;
    border: 1px solid #1f2937;
}
.small {color:#94a3b8; font-size:.85rem;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    return WorldCupAnalyticsApp(str(BASE_DIR / "world-cup-2026-team-schedules.csv"))

engine = load_engine()
df = engine.df.copy()
teams = engine.available_teams

st.markdown("""
<div class="hero">
<h1>⚽ FIFA World Cup 2026 — Team Analytics</h1>
<p>Interactive tactical telemetry, match schedule and Monte Carlo outcome simulation.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Team Selection")
    search = st.text_input("Search team", placeholder="e.g. Argentina")
    filtered = [t for t in teams if search.lower() in t.lower()] if search else teams
    if not filtered:
        st.warning("No matching team.")
        st.stop()
    team = st.selectbox("Select team", filtered, index=0)
    simulations = st.slider("Monte Carlo simulations", 1000, 25000, 10000, 1000)
    st.caption(f"{len(teams)} teams available in the schedule dataset.")

team_rows = df[df.team_name == team].drop_duplicates("match_id").copy()
if team_rows.empty:
    st.error("Team not found in the uploaded schedule dataset.")
    st.stop()

rating = engine._get_rating(team)
first_opp = team_rows.iloc[0]["opponent_name"]

# Run the original project's calculations.
with st.spinner("Running analytics..."):
    passes, shots = engine.generate_telemetry(team, first_opp)
    probs = engine.simulate_win_probabilities(team, num_sims=simulations)

# Header metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Team", f'{team_rows.iloc[0]["team_flag"]} {team}')
c2.metric("FIFA Rating", rating)
c3.metric("Group", str(team_rows.iloc[0]["group"]))
c4.metric("Group Matches", len(team_rows))

st.divider()

def pitch_base(title):
    fig = go.Figure()
    line = "#94a3b8"
    # Outer boundary
    for x0, y0, x1, y1 in [(0,0,120,0),(120,0,120,80),(120,80,0,80),(0,80,0,0),
                           (60,0,60,80)]:
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=line, width=2))
    fig.add_shape(type="circle", x0=50.85, y0=30.85, x1=69.15, y1=49.15,
                  line=dict(color=line, width=2))
    for x0, y0, x1, y1 in [(0,18,18,18),(18,18,18,62),(18,62,0,62),
                           (102,18,120,18),(102,18,102,62),(102,62,120,62),
                           (0,30,6,30),(6,30,6,50),(6,50,0,50),
                           (114,30,120,30),(114,30,114,50),(114,50,120,50)]:
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=line, width=2))
    fig.update_layout(
        title=title, height=480,
        paper_bgcolor="#111827", plot_bgcolor="#0f172a",
        margin=dict(l=10,r=10,t=55,b=10),
        xaxis=dict(range=[-2,122], visible=False),
        yaxis=dict(range=[-2,82], visible=False, scaleanchor="x", scaleratio=1),
        showlegend=True, font=dict(color="white")
    )
    return fig

tab1, tab2, tab3 = st.tabs(["📊 Overview", "🗓️ Schedule", "📋 Data"])

with tab1:
    left, right = st.columns(2)

    with left:
        fig = pitch_base(f"{team} — Pass Telemetry vs {first_opp}")
        sample = passes.sample(min(65, len(passes)), random_state=42)
        for _, p in sample.iterrows():
            fig.add_annotation(
                x=float(p["end_x"]), y=float(p["end_y"]),
                ax=float(p["x"]), ay=float(p["y"]),
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=.7,
                arrowwidth=1, arrowcolor="#38bdf8"
            )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        fig = pitch_base(f"{team} — Shot Map & xG vs {first_opp}")
        miss = shots[~shots["is_goal"]]
        goals = shots[shots["is_goal"]]
        if len(miss):
            fig.add_trace(go.Scatter(
                x=miss["x"], y=miss["y"], mode="markers",
                name="Shot (Miss/Save)",
                marker=dict(size=(miss["xg"]*28+8), symbol="circle",
                            line=dict(width=1, color="white")),
                text=[f"xG: {x:.3f}" for x in miss["xg"]],
                hovertemplate="%{text}<extra></extra>"
            ))
        if len(goals):
            fig.add_trace(go.Scatter(
                x=goals["x"], y=goals["y"], mode="markers",
                name="Goal",
                marker=dict(size=(goals["xg"]*34+12), symbol="star",
                            line=dict(width=1, color="white")),
                text=[f"xG: {x:.3f}" for x in goals["xg"]],
                hovertemplate="%{text}<extra></extra>"
            ))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Monte Carlo outcome probabilities")
    p_long = probs.melt(id_vars="Opponent", var_name="Outcome", value_name="Probability")
    chart = go.Figure()
    for outcome in ["Win %", "Draw %", "Loss %"]:
        sub = p_long[p_long["Outcome"] == outcome]
        chart.add_trace(go.Bar(x=sub["Opponent"], y=sub["Probability"], name=outcome,
                               text=[f"{v:.1f}%" for v in sub["Probability"]],
                               textposition="outside"))
    chart.update_layout(
        barmode="group", height=430, yaxis=dict(range=[0,100], title="Probability (%)"),
        paper_bgcolor="#111827", plot_bgcolor="#0f172a", font=dict(color="white"),
        margin=dict(l=20,r=20,t=35,b=20)
    )
    st.plotly_chart(chart, use_container_width=True)
    st.caption(f"Simulation count: {simulations:,}. These are model simulations, not official FIFA predictions.")

with tab2:
    st.subheader(f"{team} — World Cup 2026 schedule")
    schedule = team_rows[["match_id","stage_name","group","venue","taipei_date","taipei_time",
                          "is_home","opponent_name","opponent_flag","match_url","live_score_url"]].copy()
    schedule["Venue"] = schedule.apply(lambda r: ("Home" if r["is_home"] else "Away"), axis=1)
    schedule["Opponent"] = schedule["opponent_flag"] + " " + schedule["opponent_name"]
    schedule = schedule.rename(columns={
        "match_id":"Match","stage_name":"Stage","group":"Group",
        "taipei_date":"Date","taipei_time":"Time"
    })
    st.dataframe(
        schedule[["Match","Stage","Group","Date","Time","Venue","Opponent","venue","match_url","live_score_url"]],
        use_container_width=True, hide_index=True,
        column_config={
            "match_url": st.column_config.LinkColumn("Match"),
            "live_score_url": st.column_config.LinkColumn("Live score"),
        }
    )

with tab3:
    st.subheader("Underlying dataset")
    st.write(f"Showing {len(team_rows)} unique matches for **{team}** from the uploaded CSV.")
    st.dataframe(team_rows, use_container_width=True, hide_index=True)

st.divider()
st.caption("Frontend built around the supplied Python analytics class and uploaded World Cup schedule CSV.")
