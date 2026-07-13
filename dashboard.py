# dashboard.py
# This turns our attack_log.jsonl file into a live visual dashboard.
# Run with: streamlit run dashboard.py

import json
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="AI Defending AI - Dashboard", layout="wide")

LOG_FILE = "attack_log.jsonl"


def load_logs():
    """Reads attack_log.jsonl (one JSON object per line) into a pandas table."""
    if not Path(LOG_FILE).exists():
        return pd.DataFrame()

    rows = []
    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return pd.DataFrame(rows)


st.title("🛡️ AI Defending AI — Live Security Dashboard")
st.caption("Real-time monitoring of prompt injection attempts against our AI firewall")

df = load_logs()

if df.empty:
    st.warning("No attack data yet. Run `python attacker.py` first, then refresh this page.")
    st.stop()

# ---- TOP METRICS ----
total_requests = len(df)
blocked_input = (df["stage_blocked"] == "input_filter").sum()
blocked_output = (df["stage_blocked"] == "output_filter").sum()
leaked = df["leaked"].sum()
clean = total_requests - blocked_input - blocked_output - leaked

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Requests", total_requests)
col2.metric("Blocked at Input", int(blocked_input))
col3.metric("Blocked at Output", int(blocked_output))
col4.metric("🔴 Leaked", int(leaked))

defense_rate = round(((total_requests - leaked) / total_requests) * 100, 1) if total_requests else 0
st.subheader(f"Overall Defense Rate: {defense_rate}%")
st.progress(defense_rate / 100)

st.divider()

# ---- CHART 1: Outcomes breakdown ----
left, right = st.columns(2)

with left:
    st.subheader("Outcome Breakdown")
    outcome_counts = {
        "Blocked at Input": int(blocked_input),
        "Blocked at Output": int(blocked_output),
        "Leaked": int(leaked),
        "Clean/Allowed": int(clean),
    }
    fig1 = px.pie(
        names=list(outcome_counts.keys()),
        values=list(outcome_counts.values()),
        color=list(outcome_counts.keys()),
        color_discrete_map={
            "Blocked at Input": "#2ecc71",
            "Blocked at Output": "#f1c40f",
            "Leaked": "#e74c3c",
            "Clean/Allowed": "#3498db",
        }
    )
    st.plotly_chart(fig1, use_container_width=True)

# ---- CHART 2: Which attack rules fired most ----
with right:
    st.subheader("Most Triggered Firewall Rules")
    all_rules = []
    for rules_list in df["matched_rules"]:
        all_rules.extend(rules_list)

    if all_rules:
        rule_counts = pd.Series(all_rules).value_counts().reset_index()
        rule_counts.columns = ["Rule", "Times Triggered"]
        fig2 = px.bar(rule_counts, x="Times Triggered", y="Rule", orientation="h")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No rules triggered yet.")

st.divider()

# ---- FULL LOG TABLE ----
st.subheader("📋 Full Attack Log")
display_df = df[["timestamp", "user_message", "stage_blocked", "leaked", "matched_rules"]]
st.dataframe(display_df, use_container_width=True)