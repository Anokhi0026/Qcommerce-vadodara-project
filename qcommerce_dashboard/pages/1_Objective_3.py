import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import (
    load_data, get_product_categories, get_kruskal_results,
    get_spearman_corr, run_chi_square,
    AGE_ORDER, TENURE_ORDER, ORDER_ORDER, TIME_ORDER,
    PAY_ORDER, APP_ORDER
)

st.set_page_config(page_title="Obj 3 — Usage Behavior", layout="wide")

df, users, non_users = load_data()

# ---------------- CHART STYLE ----------------
COLORS = ["#6C63FF", "#FF6B6B", "#4ADE80", "#FBBF24", "#38BDF8"]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB"),
    margin=dict(t=30, b=10, l=10, r=10)
)

# ---------------- SECTION 1 ----------------
st.title("Usage Behavior Patterns")

c1, c2 = st.columns(2)

with c1:
    app_counts = users["App_Used"].value_counts().reindex(APP_ORDER).fillna(0)

    fig = go.Figure(go.Bar(
        x=app_counts.index,
        y=app_counts.values,
        marker_color=COLORS,
        text=[f"{v:.0f}" for v in app_counts.values],
        textposition="outside"
    ))

    fig.update_layout(**CHART_LAYOUT, title="Primary App Used")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

    st.plotly_chart(fig, width="stretch")

with c2:
    tenure_col = "How long have you been using Q-Commerce apps?"
    ten = users[tenure_col].value_counts().reindex(TENURE_ORDER).fillna(0)

    fig = go.Figure(go.Bar(
        x=ten.index,
        y=ten.values,
        marker_color=COLORS,
        text=[f"{v:.0f}" for v in ten.values],
        textposition="outside"
    ))

    fig.update_layout(**CHART_LAYOUT, title="Usage Tenure")
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

    st.plotly_chart(fig, width="stretch")

# ---------------- SECTION 2: CHI-SQUARE ----------------
st.header("Chi-Square Analysis")

behavior_map = {
    "App_Used": "App Used",
    "average order value": "Order Value",
    "preferred delivery time": "Delivery Time",
    "preferred payment method?": "Payment"
}

demo_map = {
    "Age_Group": "Age",
    "Income": "Income",
    "Occupation": "Occupation"
}

rows = []

for bcol, blabel in behavior_map.items():
    for dcol, dlabel in demo_map.items():
        try:
            r = run_chi_square(bcol, dcol)
            rows.append({
                "Behavior": blabel,
                "Demographic": dlabel,
                "Cramér's V": r["v"],
                "p-value": r["p"],
                "Significant": "Yes" if r["sig"] else "No"
            })
        except:
            pass

chi_df = pd.DataFrame(rows)

# ---------------- FIXED PIVOT ----------------
pivot = chi_df.pivot_table(
    index="Behavior",
    columns="Demographic",
    values="Cramér's V",
    aggfunc="mean"
).fillna(0)

pivot_p = chi_df.pivot_table(
    index="Behavior",
    columns="Demographic",
    values="p-value",
    aggfunc="mean"
).fillna(1)

# ---------------- FIXED ANNOTATIONS ----------------
annots = [[
    f"{pivot.loc[r, c]:.2f}"
    f"{'**' if pivot_p.loc[r,c]<0.01 else '*' if pivot_p.loc[r,c]<0.05 else ''}"
    for c in pivot.columns
] for r in pivot.index]

fig_hm = go.Figure(go.Heatmap(
    z=pivot.values,
    x=pivot.columns,
    y=pivot.index,
    text=annots,
    texttemplate="%{text}",
    colorscale="Purples"
))

fig_hm.update_layout(
    **CHART_LAYOUT,
    title="Cramér's V Heatmap"
)

st.plotly_chart(fig_hm, width="stretch")

# ---------------- TABLE (FIXED applymap) ----------------
st.subheader("Chi-Square Results Table")
st.dataframe(chi_df, width="stretch")

# ---------------- SECTION 3: SATISFACTION ----------------
st.header("Satisfaction Analysis")

sat_col = "Overall satisfaction with Q-Commerce Apps"
data = users[sat_col].dropna()

st.metric("Mean Satisfaction", f"{data.mean():.2f} / 5")

# Distribution
counts = data.value_counts().sort_index()

fig = go.Figure(go.Bar(
    x=counts.index,
    y=counts.values,
    marker_color="#6C63FF"
))

fig.update_layout(**CHART_LAYOUT, title="Satisfaction Distribution")
fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)")
fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)")

st.plotly_chart(fig, width="stretch")

# ---------------- CORRELATION ----------------
corr_df, _ = get_spearman_corr()

fig_corr = go.Figure(go.Heatmap(
    z=corr_df.values,
    x=corr_df.columns,
    y=corr_df.index,
    colorscale="Purples"
))

fig_corr.update_layout(**CHART_LAYOUT, title="Correlation Matrix")

st.plotly_chart(fig_corr, width="stretch")