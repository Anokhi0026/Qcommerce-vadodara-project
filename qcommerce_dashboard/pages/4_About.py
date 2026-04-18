import streamlit as st

st.set_page_config(page_title="About & Methods", page_icon="ℹ️",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
h1,h2,h3,h4{font-family:'Syne',sans-serif!important;font-weight:700!important;}
.section-header{font-family:'Syne',sans-serif;font-size:0.72rem;font-weight:600;
    color:#6C63FF;text-transform:uppercase;letter-spacing:0.15em;margin-bottom:8px;}
.finding-card{background:#1A1A2E;border-left:3px solid #6C63FF;
    border-radius:0 12px 12px 0;padding:16px 20px;margin:8px 0;}
.finding-card h4{font-family:'Syne',sans-serif!important;font-size:0.95rem!important;
    color:#E8E8F0!important;margin:0 0 6px 0!important;}
.finding-card p{font-size:0.85rem;color:#9999BB;margin:0;line-height:1.6;}
.test-row{display:flex;align-items:flex-start;gap:12px;padding:10px 0;
    border-bottom:1px solid rgba(108,99,255,0.1);}
.test-num{font-family:'Syne',sans-serif;font-size:0.75rem;font-weight:700;
    color:#6C63FF;min-width:28px;padding-top:2px;}
.test-name{font-size:0.88rem;color:#E8E8F0;font-weight:500;}
.test-desc{font-size:0.8rem;color:#9999BB;margin-top:2px;}
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

st.markdown("""
<h1 style='font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;
    color:#E8E8F0;margin:4px 0 8px;'>About & Methods</h1>
<p style='color:#9999BB;max-width:680px;line-height:1.7;font-size:0.95rem;'>
Research design, data collection methodology, and complete list of statistical tests used.
</p>
""", unsafe_allow_html=True)

c_left, c_right = st.columns(2, gap="large")

with c_left:
    st.markdown("---")
    st.markdown("<div class='section-header'>Study Details</div>", unsafe_allow_html=True)
    details = [
        ("🎓 Institution", "The Maharaja Sayajirao University of Baroda, Vadodara"),
        ("📚 Department", "Department of Statistics"),
        ("🎯 Degree", "Master of Science (Statistics)"),
        ("📍 Study Area", "Vadodara, Gujarat, India"),
        ("📅 Study Year", "2024–25"),
        ("📋 Topic", "Consumer Usage and Adoption of Q-Commerce Applications in Vadodara"),
        ("👥 Sample Size", "341 respondents (228 users + 113 non-users)"),
        ("🔧 Data Collection", "Structured questionnaire via Google Forms"),
        ("📊 Sampling", "Convenience sampling, Vadodara residents"),
    ]
    for icon_label, value in details:
        st.markdown(f"""
        <div class='finding-card'>
            <h4>{icon_label}</h4>
            <p>{value}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Questionnaire Structure (8 pages)</div>",
                unsafe_allow_html=True)
    pages = [
        ("Page 1", "Demographics — Age, Gender, Education, Occupation, Income; Q-Commerce awareness"),
        ("Page 2", "User Section — App used, tenure, order value, delivery time, payment method"),
        ("Page 3", "Products ordered; Likert scale (10 adoption driver items, 5-point scale)"),
        ("Page 4", "Satisfaction (1–5), continuity likelihood, recommendation likelihood; biggest reason"),
        ("Page 5", "Non-User Section — Reasons for non-use; 7-item barrier Likert scale"),
        ("Pages 6–8", "Extended barrier items; willingness to adopt under conditions; family usage"),
    ]
    for pg, desc in pages:
        st.markdown(f"""
        <div class='finding-card'>
            <h4>{pg}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)

with c_right:
    st.markdown("---")
    st.markdown("<div class='section-header'>Complete List of Statistical Tests</div>",
                unsafe_allow_html=True)

    tests = [
        ("01", "Chi-Square Test of Independence",
         "Objective 2 & 3 — Demographic × adoption/behavior associations (20 pairs)"),
        ("02", "Cramér's V",
         "Effect size for chi-square tests; bias-corrected formula used"),
        ("03", "Kruskal-Wallis H Test",
         "Obj 3 — Satisfaction scores across age, income, occupation, app used"),
        ("04", "Dunn's Post-Hoc Test (Bonferroni)",
         "Obj 3 — Pairwise comparisons after significant Kruskal-Wallis"),
        ("05", "Spearman Rank Correlation",
         "Obj 3 — Satisfaction ↔ Continuity ↔ Recommendation interdependence"),
        ("06", "Cronbach's Alpha",
         "Obj 4 — Internal reliability of 10-item Likert adoption driver scale"),
        ("07", "Corrected Item-Total Correlation",
         "Obj 4 — With alpha-if-deleted for each item"),
        ("08", "KMO Test (Kaiser-Meyer-Olkin)",
         "Obj 4 — Sampling adequacy check before EFA"),
        ("09", "Bartlett's Test of Sphericity",
         "Obj 4 — Tests if correlation matrix ≠ identity matrix"),
        ("10", "Principal Component Analysis",
         "Obj 4 — Initial factor extraction for EFA"),
        ("11", "Varimax Rotation (EFA)",
         "Obj 4 — Orthogonal rotation to improve interpretability of factor structure"),
        ("12", "Communality Analysis",
         "Obj 4 — Proportion of variance per item explained by retained factors"),
        ("13", "Kruskal-Wallis (Non-user barriers × Age)",
         "Obj 4 — Barrier strength differences by age group"),
        ("14", "Mann-Whitney U (Barriers × Gender)",
         "Obj 4 — Gender differences in barrier item scores"),
        ("15", "Mann-Whitney U with Rank-Biserial r",
         "Obj 5 — Pre-model: Users vs Non-users on Age, Education, Income"),
        ("16", "Binary Logistic Regression — Model 1",
         "Obj 5 — Demographics-only adoption prediction model"),
        ("17", "Bootstrap 95% Confidence Intervals (300 resamples)",
         "Obj 5 — CI for Odds Ratios (non-parametric, no distributional assumption)"),
        ("18", "Nagelkerke Pseudo-R²",
         "Obj 5 — Variance in adoption status explained by the model"),
        ("19", "ROC Curve & AUC",
         "Obj 5 — Discrimination ability of the logistic model"),
        ("20", "Youden's J Optimal Threshold",
         "Obj 5 — Best sensitivity/specificity trade-off classification threshold"),
        ("21", "Stratified 5-Fold Cross-Validated AUC",
         "Obj 5 — Generalisation performance, corrects for overfitting"),
        ("22", "Binary Logistic Regression — Model 2",
         "Obj 5 — Extended model: Demographics + EFA factor scores"),
        ("23", "Model Comparison (ΔR², ΔAUC)",
         "Obj 5 — Incremental predictive value of attitudinal factors over demographics"),
    ]

    for num, name, desc in tests:
        st.markdown(f"""
        <div class='test-row'>
            <div class='test-num'>{num}</div>
            <div>
                <div class='test-name'>{name}</div>
                <div class='test-desc'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div class='section-header'>Tech Stack</div>", unsafe_allow_html=True)

tech_cols = st.columns(5)
tech = [
    ("🐍", "Python 3.11", "Core language"),
    ("⚡", "Streamlit", "Dashboard framework"),
    ("📊", "Plotly", "Interactive charts"),
    ("🔢", "SciPy / NumPy", "Statistical tests"),
    ("🤖", "scikit-learn", "Machine learning"),
]
for col, (icon, name, role) in zip(tech_cols, tech):
    col.markdown(f"""
    <div style='background:#1A1A2E;border:1px solid rgba(108,99,255,0.2);
        border-radius:12px;padding:16px;text-align:center;'>
        <div style='font-size:1.5rem;'>{icon}</div>
        <div style='font-family:Syne,sans-serif;font-size:0.9rem;color:#E8E8F0;
            font-weight:600;margin:6px 0 2px;'>{name}</div>
        <div style='font-size:0.75rem;color:#9999BB;'>{role}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;color:#4A4A6A;font-size:0.78rem;padding:30px 0 10px;'>
    Department of Statistics · The Maharaja Sayajirao University of Baroda ·
    Built with Streamlit · Deployed on Streamlit Cloud
</div>
""", unsafe_allow_html=True)
