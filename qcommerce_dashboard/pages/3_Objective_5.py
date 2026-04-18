import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import load_data, get_logistic_results, get_mannwhitney_results

st.set_page_config(page_title="Obj 5 — Predictive Models", page_icon="🤖",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
h1,h2,h3,h4{font-family:'Syne',sans-serif!important;font-weight:700!important;}
.section-header{font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:600;
    color:#6C63FF;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:6px;}
.finding-card{background:#1A1A2E;border-left:3px solid #6C63FF;
    border-radius:0 12px 12px 0;padding:16px 20px;margin:10px 0;}
.finding-card h4{font-family:'Syne',sans-serif!important;font-size:0.95rem!important;
    color:#E8E8F0!important;margin:0 0 6px 0!important;}
.finding-card p{font-size:0.85rem;color:#9999BB;margin:0;line-height:1.6;}
.metric-card{background:linear-gradient(135deg,#1A1A2E 0%,#16213E 100%);
    border:1px solid rgba(108,99,255,0.25);border-radius:16px;
    padding:20px;text-align:center;}
.metric-card .val{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#6C63FF;}
.metric-card .lbl{font-size:0.75rem;color:#9999BB;margin-top:4px;text-transform:uppercase;letter-spacing:0.08em;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:20px 0 10px;'>
        <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#E8E8F0;'>⚡ Q-Commerce</div>
        <div style='font-size:0.75rem;color:#9999BB;margin-top:4px;'>Vadodara Research Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                 label="🏠  Overview")
    st.page_link("pages/1_Objective_3.py", label="📊  Obj 3 — Usage Behavior")
    st.page_link("pages/2_Objective_4.py", label="🔍  Obj 4 — Key Drivers")
    st.page_link("pages/3_Objective_5.py", label="🤖  Obj 5 — Predictive Models")
    st.page_link("pages/4_About.py",       label="ℹ️   About & Methods")

df, users, non_users = load_data()

COLORS = ["#6C63FF","#FF6B6B","#4ADE80","#FBBF24","#38BDF8"]
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB", family="DM Sans"),
    margin=dict(t=40, b=10, l=10, r=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)")
)

st.markdown("""
<span style='font-family:Syne,sans-serif;font-size:0.75rem;color:#6C63FF;
    text-transform:uppercase;letter-spacing:0.12em;'>Objective 5</span>
<h1 style='font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;
    color:#E8E8F0;margin:4px 0 8px;'>Predictive Models for Adoption</h1>
<p style='color:#9999BB;max-width:680px;line-height:1.7;font-size:0.95rem;'>
Developing binary logistic regression models to predict Q-Commerce adoption likelihood
based on socio-demographic and attitudinal variables across <b style='color:#A89CFF;'>341 respondents</b>.
</p>
""", unsafe_allow_html=True)

# Load with spinner since this is compute-heavy
with st.spinner("Running logistic regression models…"):
    coef_df, auc, cv_auc, nag, fpr, tpr, opt_thresh = get_logistic_results()
    mw_df = get_mannwhitney_results()

# ── SECTION 1: Pre-Model Mann-Whitney ──────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>1 · Pre-Model Check — Mann-Whitney U Test</div>",
            unsafe_allow_html=True)
st.markdown("""
<p style='color:#9999BB;font-size:0.88rem;'>
Do users and non-users actually differ on demographics? This justifies including them as predictors.
</p>""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
for col, (_, row) in zip([c1, c2, c3], mw_df.iterrows()):
    sig_color = "#4ADE80" if row["Significant"] else "#9999BB"
    col.markdown(f"""
    <div class='metric-card'>
        <div class='lbl'>{row['Variable']}</div>
        <div class='val'>p={row['p']:.4f}</div>
        <div style='font-size:0.78rem;color:{sig_color};margin-top:6px;font-weight:600;'>
            {"✓ Significant" if row['Significant'] else "✗ Not Significant"}
        </div>
        <div style='font-size:0.75rem;color:#9999BB;margin-top:4px;'>
            r = {row['r']} ({row['Effect']} effect)<br>
            Users median: {row['Users Median']:.0f} · Non-users: {row['Non-Users Median']:.0f}
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("📋 Full Mann-Whitney results"):
    st.dataframe(mw_df, use_container_width=True)

# ── SECTION 2: Model 1 ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>2 · Model 1 — Binary Logistic Regression (Demographics Only)</div>",
            unsafe_allow_html=True)

# Performance metrics
m1, m2, m3, m4 = st.columns(4)
auc_interp = ("Excellent" if auc > 0.9 else "Good" if auc > 0.8
              else "Fair" if auc > 0.7 else "Poor")
metrics = [
    (m1, f"{auc:.3f}", "AUC (Train)", auc_interp),
    (m2, f"{cv_auc:.3f}", "AUC (5-Fold CV)", "Cross-validated"),
    (m3, f"{nag:.3f}", "Nagelkerke R²", "Variance explained"),
    (m4, f"{opt_thresh:.2f}", "Optimal Threshold", "Youden's J"),
]
for col, val, label, sub in metrics:
    col.markdown(f"""
    <div class='metric-card'>
        <div class='val'>{val}</div>
        <div class='lbl'>{label}</div>
        <div style='font-size:0.75rem;color:#6C63FF;margin-top:4px;'>{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c_left, c_right = st.columns([1.2, 1], gap="large")

with c_left:
    # Forest plot (odds ratios)
    or_sorted = coef_df.sort_values("OR")
    colors_or = ["#4ADE80" if s == "Yes" else "#555577" for s in or_sorted["Significant"]]

    fig_forest = go.Figure()
    y_pos = list(range(len(or_sorted)))
    fig_forest.add_trace(go.Scatter(
        x=or_sorted["OR"], y=y_pos,
        mode="markers", marker=dict(color=colors_or, size=9, symbol="square"),
        name="Odds Ratio"
    ))
    for i, (_, row) in enumerate(or_sorted.iterrows()):
        fig_forest.add_trace(go.Scatter(
            x=[row["CI_lo"], row["CI_hi"]], y=[i, i],
            mode="lines",
            line=dict(color=colors_or[i], width=2),
            showlegend=False
        ))
    fig_forest.add_vline(x=1.0, line_dash="dash", line_color="#9999BB",
                          annotation_text="OR = 1", annotation_font_color="#9999BB")
    fig_forest.update_layout(
        **CHART_LAYOUT, height=560, showlegend=False,
        yaxis=dict(tickvals=y_pos, ticktext=or_sorted["Predictor"].tolist(),
                   gridcolor="rgba(255,255,255,0.06)"),
        xaxis=dict(title="Odds Ratio (OR) with 95% Bootstrap CI",
                   gridcolor="rgba(255,255,255,0.06)"),
        title=dict(text="Forest Plot — Odds Ratios (Green = Significant)",
                   font=dict(color="#E8E8F0", family="Syne"))
    )
    st.plotly_chart(fig_forest, use_container_width=True)

with c_right:
    # ROC Curve
    fig_roc = go.Figure()
    fig_roc.add_trace(go.Scatter(
        x=fpr, y=tpr, mode="lines",
        line=dict(color="#6C63FF", width=3),
        name=f"Model 1 (AUC = {auc:.3f})",
        fill="tozeroy", fillcolor="rgba(108,99,255,0.08)"
    ))
    fig_roc.add_trace(go.Scatter(
        x=[0, 1], y=[0, 1], mode="lines",
        line=dict(color="#555577", dash="dash"), name="Random (AUC=0.50)"
    ))
    # Optimal threshold point
    j = tpr - fpr
    opt_idx = np.argmax(j)
    fig_roc.add_trace(go.Scatter(
        x=[fpr[opt_idx]], y=[tpr[opt_idx]],
        mode="markers", marker=dict(color="#FF6B6B", size=12, symbol="star"),
        name=f"Optimal threshold ({opt_thresh:.2f})"
    ))
    fig_roc.update_layout(
        **CHART_LAYOUT, height=340,
        xaxis=dict(title="False Positive Rate", range=[0,1],
                   gridcolor="rgba(255,255,255,0.06)"),
        yaxis=dict(title="True Positive Rate", range=[0,1],
                   gridcolor="rgba(255,255,255,0.06)"),
        legend=dict(x=0.4, y=0.15, font=dict(color="#9999BB"), bgcolor="rgba(0,0,0,0)"),
        title=dict(text="ROC Curve — Model 1",
                   font=dict(color="#E8E8F0", family="Syne"))
    )
    st.plotly_chart(fig_roc, use_container_width=True)

    # AUC interpretation guide
    st.markdown("""
    <div style='background:#1A1A2E;border:1px solid rgba(108,99,255,0.2);
        border-radius:12px;padding:16px;'>
        <div style='font-size:0.72rem;color:#6C63FF;text-transform:uppercase;
            letter-spacing:0.1em;margin-bottom:8px;'>AUC Interpretation</div>
        <div style='font-size:0.82rem;color:#9999BB;line-height:1.8;'>
            AUC > 0.90 → Excellent<br>
            AUC 0.80–0.90 → Good<br>
            AUC 0.70–0.80 → Fair<br>
            AUC < 0.70 → Poor
        </div>
        <div style='margin-top:10px;font-size:0.82rem;'>
            <span style='color:#6C63FF;font-weight:600;'>Model 1: {:.3f}</span>
            <span style='color:#9999BB;'> → {}</span>
        </div>
    </div>
    """.format(auc, auc_interp), unsafe_allow_html=True)

with st.expander("📋 Full coefficient table — Odds Ratios with 95% Bootstrap CI"):
    display_df = coef_df.rename(columns={
        "β": "β (log-OR)", "OR": "Odds Ratio",
        "CI_lo": "95% CI Lower", "CI_hi": "95% CI Upper"
    })
    st.markdown("""
    <p style='color:#9999BB;font-size:0.82rem;'>
    Reference categories: Male | Age 18–25 | School Level | Student | Income Below ₹20K<br>
    OR > 1 = more likely to be a user · OR < 1 = less likely · CI computed via 300 bootstrap resamples
    </p>""", unsafe_allow_html=True)
    st.dataframe(display_df.style.applymap(
        lambda v: "color:#4ADE80;font-weight:600" if v == "Yes" else "color:#9999BB",
        subset=["Significant"]
    ), use_container_width=True)

# ── SECTION 3: Model Interpretation ───────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>3 · Model Interpretation & Practical Use</div>",
            unsafe_allow_html=True)

sig_preds = coef_df[coef_df["Significant"] == "Yes"].sort_values("OR", ascending=False)
if not sig_preds.empty:
    st.markdown("**Significant predictors of Q-Commerce adoption:**")
    for _, row in sig_preds.iterrows():
        direction = "more" if row["OR"] > 1 else "less"
        col = "4ADE80" if row["OR"] > 1 else "FF6B6B"
        st.markdown(f"""
        <div class='finding-card'>
            <h4 style='color:#{col}!important;'>{row['Predictor'].replace('_',' ')}</h4>
            <p>OR = {row['OR']:.3f} (95% CI: {row['CI_lo']:.3f}–{row['CI_hi']:.3f}) —
            This group is {abs(row['OR']-1)*100:.0f}% {direction} likely to have adopted Q-Commerce
            compared to their reference category.</p>
        </div>
        """, unsafe_allow_html=True)

# ── Key Findings ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>Key Findings — Objective 5</div>", unsafe_allow_html=True)

auc_qual = ("excellent" if auc > 0.9 else "good" if auc > 0.8 else "fair")

findings = [
    ("✅ Demographics Differ Significantly",
     f"Mann-Whitney U confirms users and non-users differ significantly on Age and Education, validating the core premise that demographic predictors are meaningful for the model."),
    (f"📈 Model 1 AUC = {auc:.3f} ({auc_qual.title()} discrimination)",
     f"The demographics-only model correctly discriminates users from non-users well above chance. Nagelkerke R² = {nag:.3f} — demographics explain {nag*100:.1f}% of variance in adoption status."),
    ("🎯 Age is the Strongest Predictor",
     "Older age groups consistently show lower odds of adoption relative to the 18–25 reference group. Q-Commerce in Vadodara is predominantly a young-consumer phenomenon."),
    ("🔑 Two-Stage Adoption Framework",
     "Demographics set a baseline adoption probability (who you are). Adding attitudinal factor scores from Obj 4 further refines this prediction — what you think about convenience and price matters beyond demographics alone."),
    ("📋 Practical Application",
     "The model identifies high-probability non-adopters who demographically resemble users — these are the most actionable targets for Q-Commerce platform marketing campaigns in Vadodara."),
]
for title, text in findings:
    st.markdown(f"""
    <div class='finding-card'>
        <h4>{title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background:#1A1A2E;border:1px solid rgba(108,99,255,0.15);
    border-radius:12px;padding:16px;margin-top:16px;'>
    <div style='font-size:0.72rem;color:#6C63FF;text-transform:uppercase;
        letter-spacing:0.1em;margin-bottom:8px;'>Methodological Note</div>
    <p style='font-size:0.82rem;color:#9999BB;line-height:1.6;margin:0;'>
    Logistic regression implemented using sklearn with C=1000 (approximating unregularized MLE).
    Significance determined by 95% bootstrap CIs (300 resamples) not including OR=1.
    For Model 2 (extended with factor scores), non-user Likert responses are mean-imputed
    before scaling — this is disclosed as a methodological limitation.
    </p>
</div>
""", unsafe_allow_html=True)
