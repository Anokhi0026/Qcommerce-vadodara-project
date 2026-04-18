import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data_loader import load_data, AGE_ORDER, INCOME_ORDER

st.set_page_config(
    page_title="Q-Commerce Vadodara | Research Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

.main { background: #0F0F1A; }

.stSidebar {
    background: linear-gradient(180deg, #13132A 0%, #0F0F1A 100%) !important;
    border-right: 1px solid rgba(108, 99, 255, 0.2);
}

.stSidebar .stMarkdown p {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: #9999BB;
}

.metric-card {
    background: linear-gradient(135deg, #1A1A2E 0%, #16213E 100%);
    border: 1px solid rgba(108, 99, 255, 0.25);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: border-color 0.3s;
}
.metric-card:hover { border-color: rgba(108, 99, 255, 0.6); }
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    color: #6C63FF;
    line-height: 1;
}
.metric-card .label {
    font-size: 0.8rem;
    color: #9999BB;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-card .sub {
    font-size: 0.75rem;
    color: #6C63FF;
    margin-top: 4px;
    opacity: 0.8;
}

.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: #6C63FF;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 6px;
}

.finding-card {
    background: #1A1A2E;
    border-left: 3px solid #6C63FF;
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 10px 0;
}
.finding-card h4 {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    color: #E8E8F0 !important;
    margin: 0 0 6px 0 !important;
}
.finding-card p {
    font-size: 0.85rem;
    color: #9999BB;
    margin: 0;
    line-height: 1.6;
}

.hero-badge {
    display: inline-block;
    background: rgba(108, 99, 255, 0.15);
    border: 1px solid rgba(108, 99, 255, 0.4);
    color: #A89CFF;
    font-size: 0.75rem;
    font-family: 'DM Sans', sans-serif;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 12px;
    letter-spacing: 0.05em;
}

.obj-chip {
    display: inline-block;
    background: rgba(108, 99, 255, 0.12);
    border: 1px solid rgba(108, 99, 255, 0.3);
    color: #A89CFF;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.8rem;
    margin: 4px;
}

.stExpander {
    background: #1A1A2E !important;
    border: 1px solid rgba(108, 99, 255, 0.2) !important;
    border-radius: 12px !important;
}

div[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    color: #6C63FF !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px;'>
        <div style='font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#E8E8F0;'>⚡ Q-Commerce</div>
        <div style='font-size:0.75rem; color:#9999BB; margin-top:4px;'>Vadodara Research Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div class='section-header'>Navigation</div>", unsafe_allow_html=True)
    st.page_link("app.py",             label="🏠  Overview",             )
    st.page_link("pages/1_Objective_3.py", label="📊  Obj 3 — Usage Behavior")
    st.page_link("pages/2_Objective_4.py", label="🔍  Obj 4 — Key Drivers")
    st.page_link("pages/3_Objective_5.py", label="🤖  Obj 5 — Predictive Models")
    st.page_link("pages/4_About.py",       label="ℹ️   About & Methods")

    st.markdown("---")
    st.markdown("<div class='section-header'>Study Info</div>", unsafe_allow_html=True)
    st.markdown("""
    <p>📍 Vadodara, Gujarat</p>
    <p>🎓 MSc Statistics, MS University of Baroda</p>
    <p>📅 2024–25</p>
    <p>👥 341 respondents</p>
    """, unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
df, users, non_users = load_data()

# ── Hero Section ───────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-badge'>Master's Degree Research Project • MSU Baroda</div>
<h1 style='font-family:Syne,sans-serif; font-size:2.6rem; font-weight:800;
           color:#E8E8F0; margin:0; line-height:1.15;'>
    Consumer Usage & Adoption<br>
    <span style='color:#6C63FF;'>of Q-Commerce Apps</span><br>
    in Vadodara
</h1>
<p style='color:#9999BB; font-size:1rem; max-width:680px; margin-top:14px; line-height:1.7;'>
    A statistical study examining usage patterns, adoption drivers, and predictive models
    for quick-commerce applications among 341 consumers in Vadodara, Gujarat.
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
adoption_rate = len(users) / len(df) * 100
awareness_rate = (df["Aware_QC"] == "Yes").sum() / len(df) * 100
top_app = users["App_Used"].value_counts().index[0]
top_app_pct = users["App_Used"].value_counts().iloc[0] / len(users) * 100

c1, c2, c3, c4, c5 = st.columns(5)
cards = [
    (c1, str(len(df)),         "Total Respondents",  "Vadodara, Gujarat"),
    (c2, f"{adoption_rate:.0f}%",   "Adoption Rate",      f"{len(users)} active users"),
    (c3, f"{len(non_users)}",  "Non-Users",          "Analysed separately"),
    (c4, f"{awareness_rate:.0f}%",  "Awareness Rate",     "Know Q-Commerce"),
    (c5, f"{top_app_pct:.0f}%",    f"{top_app} Share",   "Top app in Vadodara"),
]
for col, val, label, sub in cards:
    with col:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='value'>{val}</div>
            <div class='label'>{label}</div>
            <div class='sub'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Two-column layout ──────────────────────────────────────────────────────────
left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown("<div class='section-header'>Sample Composition</div>", unsafe_allow_html=True)

    # Adoption donut
    fig_donut = go.Figure(go.Pie(
        labels=["Q-Commerce Users", "Non-Users"],
        values=[len(users), len(non_users)],
        hole=0.65,
        marker_colors=["#6C63FF", "#2A2A4A"],
        textinfo="label+percent",
        textfont=dict(family="DM Sans", size=12, color="#E8E8F0"),
        hovertemplate="%{label}: %{value} respondents<extra></extra>"
    ))
    fig_donut.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        annotations=[dict(text=f"<b>{adoption_rate:.0f}%</b><br>Users",
                          x=0.5, y=0.5, font=dict(size=18, color="#E8E8F0",
                          family="Syne"), showarrow=False)]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    # Age group distribution
    st.markdown("<div class='section-header' style='margin-top:8px;'>Age Distribution</div>",
                unsafe_allow_html=True)
    age_u  = users["Age_Group"].value_counts().reindex(AGE_ORDER).fillna(0)
    age_nu = non_users["Age_Group"].value_counts().reindex(AGE_ORDER).fillna(0)

    fig_age = go.Figure()
    fig_age.add_trace(go.Bar(name="Users", x=AGE_ORDER, y=age_u.values,
                              marker_color="#6C63FF", opacity=0.9))
    fig_age.add_trace(go.Bar(name="Non-Users", x=AGE_ORDER, y=age_nu.values,
                              marker_color="#FF6B6B", opacity=0.9))
    fig_age.update_layout(
        barmode="group", paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)", height=220,
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(font=dict(color="#9999BB"), bgcolor="rgba(0,0,0,0)"),
        font=dict(color="#9999BB", family="DM Sans"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig_age, use_container_width=True)

with right:
    st.markdown("<div class='section-header'>Research Objectives</div>",
                unsafe_allow_html=True)

    objectives = [
        ("🎯", "Primary Objective",
         "Statistically analyze usage patterns and adoption behavior of Q-Commerce apps among consumers of Vadodara."),
        ("📊", "Obj 3 — Usage Behavior",
         "Examine frequency, order size, preferred delivery times, and payment methods."),
        ("🔍", "Obj 4 — Key Drivers",
         "Investigate convenience, pricing, product variety, usability, and promotions as adoption drivers."),
        ("🤖", "Obj 5 — Predictive Models",
         "Develop logistic regression models for adoption likelihood based on socio-demographic variables."),
    ]
    for icon, title, desc in objectives:
        st.markdown(f"""
        <div class='finding-card'>
            <h4>{icon} {title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Statistical Methods Used</div>",
                unsafe_allow_html=True)
    methods = ["Chi-Square & Cramér's V", "Kruskal-Wallis H Test",
               "Dunn's Post-Hoc (Bonferroni)", "Spearman Correlation",
               "Cronbach's Alpha (Reliability)", "KMO + Bartlett's Test",
               "Exploratory Factor Analysis", "Mann-Whitney U Test",
               "Binary Logistic Regression", "ROC/AUC + Nagelkerke R²",
               "Bootstrap 95% CI", "5-Fold Cross-Validation"]
    chips_html = "".join(f"<span class='obj-chip'>{m}</span>" for m in methods)
    st.markdown(chips_html, unsafe_allow_html=True)

# ── Key Findings Snapshot ──────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='section-header'>Headline Findings</div>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)
findings = [
    (f1, "Blinkit Dominates",
     "~62% of users in Vadodara use Blinkit as their primary Q-commerce app, indicating near-oligopolistic market structure."),
    (f2, "Evening is Prime Time",
     "63% of all orders are placed Evening + Night — driven by end-of-day top-up shopping, not planned grocery runs."),
    (f3, "Attitudes Predict Adoption",
     "Adding attitudinal factor scores to the logistic model substantially improves Nagelkerke R², confirming attitudes predict adoption beyond demographics."),
]
for col, title, text in findings:
    with col:
        st.markdown(f"""
        <div class='finding-card'>
            <h4>{title}</h4>
            <p>{text}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#4A4A6A; font-size:0.78rem; padding:20px 0;'>
    Department of Statistics • The Maharaja Sayajirao University of Baroda •
    Data collected via Google Forms • n = 341
</div>
""", unsafe_allow_html=True)
