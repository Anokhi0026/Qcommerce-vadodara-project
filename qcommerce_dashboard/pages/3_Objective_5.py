import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import load_data, get_logistic_results, get_mannwhitney_results

st.set_page_config(page_title="Obj 5 — Predictive Models", layout="wide")

df, users, non_users = load_data()

# ---------------- CLEAN LAYOUT ----------------
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB"),
    margin=dict(t=40, b=10, l=10, r=10)
)

st.title("Predictive Models for Adoption")

# ---------------- LOAD MODEL ----------------
coef_df, auc, cv_auc, nag, fpr, tpr, opt_thresh = get_logistic_results()
mw_df = get_mannwhitney_results()

# ---------------- MANN-WHITNEY ----------------
st.header("Mann-Whitney Test")

st.dataframe(mw_df, width="stretch")

# ---------------- MODEL METRICS ----------------
c1, c2, c3 = st.columns(3)

c1.metric("AUC", f"{auc:.3f}")
c2.metric("CV AUC", f"{cv_auc:.3f}")
c3.metric("Nagelkerke R²", f"{nag:.3f}")

# ---------------- FOREST PLOT ----------------
st.subheader("Odds Ratios")

or_sorted = coef_df.sort_values("OR")

fig = go.Figure()

y_pos = list(range(len(or_sorted)))

fig.add_trace(go.Scatter(
    x=or_sorted["OR"],
    y=y_pos,
    mode="markers",
    marker=dict(color="blue", size=8)
))

for i, row in or_sorted.iterrows():
    fig.add_trace(go.Scatter(
        x=[row["CI_lo"], row["CI_hi"]],
        y=[y_pos[list(or_sorted.index).index(i)], y_pos[list(or_sorted.index).index(i)]],
        mode="lines"
    ))

fig.add_vline(x=1)

fig.update_layout(**CHART_LAYOUT)
fig.update_yaxes(
    tickvals=y_pos,
    ticktext=or_sorted["Predictor"]
)

st.plotly_chart(fig, width="stretch")

# ---------------- ROC ----------------
st.subheader("ROC Curve")

fig = go.Figure()

fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", name="Model"))
fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Random"))

fig.update_layout(**CHART_LAYOUT)

st.plotly_chart(fig, width="stretch")

# ---------------- COEFFICIENT TABLE ----------------
st.subheader("Model Coefficients")

# ❌ REMOVED .applymap (was crashing)
st.dataframe(coef_df, width="stretch")

# ---------------- INTERPRETATION ----------------
st.subheader("Significant Predictors")

sig = coef_df[coef_df["Significant"] == "Yes"]

for _, row in sig.iterrows():
    st.write(
        f"{row['Predictor']} → OR={row['OR']:.2f} "
        f"(CI {row['CI_lo']:.2f}–{row['CI_hi']:.2f})"
    )