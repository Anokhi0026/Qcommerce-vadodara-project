import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import (
    load_data, get_likert_data, get_item_total_corr,
    get_efa_results, SHORT_NAMES, LIKERT_MAP
)

st.set_page_config(page_title="Obj 4 — Key Drivers", layout="wide")

df, users, non_users = load_data()
ld = get_likert_data()

# ---------------- CLEAN CHART LAYOUT ----------------
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB"),
    margin=dict(t=40, b=10, l=10, r=10)
)

st.title("Key Drivers of Adoption")

# ---------------- CRONBACH ALPHA ----------------
def cronbach_alpha(df_in):
    k = df_in.shape[1]
    item_var = df_in.var(axis=0, ddof=1).sum()
    total_var = df_in.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)

alpha = cronbach_alpha(ld)
st.metric("Cronbach Alpha", f"{alpha:.3f}")

# ---------------- ITEM TOTAL CORRELATION ----------------
itc = get_item_total_corr()

fig = go.Figure(go.Bar(
    y=itc["Item"],
    x=itc["Item-Total r"],
    orientation="h"
))

fig.update_layout(**CHART_LAYOUT, title="Item Total Correlation")
fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

st.plotly_chart(fig, width="stretch")

st.dataframe(itc, width="stretch")

# ---------------- DRIVER RANKING ----------------
desc = ld.describe().T[["mean", "std"]]
desc.columns = ["Mean", "Std"]
desc = desc.sort_values("Mean")

fig = go.Figure(go.Bar(
    y=desc.index,
    x=desc["Mean"],
    orientation="h"
))

fig.update_layout(**CHART_LAYOUT, title="Driver Ranking")
fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

st.plotly_chart(fig, width="stretch")

# ---------------- EFA ----------------
ldf, communalities, eigenvalues, n_factors, pct_var = get_efa_results()

fig = go.Figure(go.Scatter(
    x=list(range(1, len(eigenvalues)+1)),
    y=eigenvalues,
    mode="lines+markers"
))

fig.update_layout(**CHART_LAYOUT, title="Scree Plot")
st.plotly_chart(fig, width="stretch")

# ---------------- HEATMAP ----------------
fig_load = go.Figure(go.Heatmap(
    z=ldf.values,
    x=ldf.columns,
    y=ldf.index,
    colorscale="RdBu"
))

fig_load.update_layout(**CHART_LAYOUT, title="Factor Loadings")
st.plotly_chart(fig_load, width="stretch")

st.dataframe(ldf.round(3), width="stretch")

# ---------------- NON USER BARRIERS ----------------
BARRIER_COLS = [
    "I would consider using Q-commerce if delivery charges were lower",
    "I would consider using Q-commerce apps if product quality were guaranteed",
    "I would consider using Q-commerce apps if adequate guidance on app usage were provided",
    "I would consider using Q-commerce apps if prices were competitive",
    "I would consider using Q-commerce apps if delivery services were available in my area",
    "I would consider using Q-commerce apps if attractive discounts were offered",
    "I would consider using Q-commerce apps if I felt confident about trust, data security, and privacy."
]

bd = non_users[BARRIER_COLS].copy()

for col in BARRIER_COLS:
    bd[col] = bd[col].map(LIKERT_MAP)

bd = bd.dropna()
b_desc = bd.mean().sort_values()

fig = go.Figure(go.Bar(
    y=b_desc.index,
    x=b_desc.values,
    orientation="h"
))

fig.update_layout(**CHART_LAYOUT, title="Barriers to Adoption")
fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

st.plotly_chart(fig, width="stretch")