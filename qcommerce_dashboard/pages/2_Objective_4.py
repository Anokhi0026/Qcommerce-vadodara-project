import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import mannwhitneyu, kruskal
from data_loader import (load_data, get_likert_data, get_item_total_corr,
                          get_efa_results, SHORT_NAMES, LIKERT_MAP, LIKERT_COLS)

st.set_page_config(page_title="Obj 4 — Key Drivers", page_icon="🔍",
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
.alpha-badge{display:inline-block;font-family:'Syne',sans-serif;font-size:2rem;
    font-weight:800;color:#6C63FF;}
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
ld = get_likert_data()

COLORS = ["#6C63FF","#FF6B6B","#4ADE80","#FBBF24","#38BDF8","#F472B6"]
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB", family="DM Sans"),
    margin=dict(t=40, b=10, l=10, r=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)")
)

st.markdown("""
<span style='font-family:Syne,sans-serif;font-size:0.75rem;color:#6C63FF;
    text-transform:uppercase;letter-spacing:0.12em;'>Objective 4</span>
<h1 style='font-family:Syne,sans-serif;font-size:2.1rem;font-weight:800;
    color:#E8E8F0;margin:4px 0 8px;'>Key Drivers of Adoption</h1>
<p style='color:#9999BB;max-width:680px;line-height:1.7;font-size:0.95rem;'>
Investigating convenience, pricing, product variety, usability, and promotional offers
as drivers of Q-Commerce adoption among <b style='color:#A89CFF;'>228 users</b> and
analysing barriers among <b style='color:#A89CFF;'>113 non-users</b>.
</p>
""", unsafe_allow_html=True)

# ── SECTION 1: Cronbach's Alpha ────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>1 · Scale Reliability — Cronbach's Alpha</div>",
            unsafe_allow_html=True)

def cronbach_alpha(df_in):
    k = df_in.shape[1]
    item_var = df_in.var(axis=0, ddof=1).sum()
    total_var = df_in.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)

alpha = cronbach_alpha(ld)
interp = ("Excellent ✦" if alpha >= 0.9 else "Good ✦" if alpha >= 0.8
          else "Acceptable ✦" if alpha >= 0.7 else "Poor ✗")

c1, c2 = st.columns([1, 2])
with c1:
    st.markdown(f"""
    <div style='background:#1A1A2E;border:1px solid rgba(108,99,255,0.3);
        border-radius:16px;padding:30px;text-align:center;'>
        <div style='font-size:0.72rem;color:#9999BB;text-transform:uppercase;
            letter-spacing:0.12em;margin-bottom:8px;'>Cronbach's Alpha</div>
        <div class='alpha-badge'>α = {alpha:.3f}</div>
        <div style='margin-top:10px;font-size:0.85rem;color:#4ADE80;font-weight:600;'>{interp}</div>
        <div style='margin-top:8px;font-size:0.78rem;color:#9999BB;'>
            10 items · {len(ld)} users
        </div>
        <div style='margin-top:12px;font-size:0.75rem;color:#6C63FF;'>
            α ≥ 0.9 Excellent · ≥ 0.8 Good<br>≥ 0.7 Acceptable · < 0.7 Poor
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    itc = get_item_total_corr()
    colors_bar = ["#FF6B6B" if r < 0.3 else "#4ADE80" for r in itc["Item-Total r"]]
    itc_sorted = itc.sort_values("Item-Total r")
    fig = go.Figure(go.Bar(
        y=itc_sorted["Item"], x=itc_sorted["Item-Total r"],
        orientation="h", marker_color=colors_bar,
        text=[f"{v:.3f}" for v in itc_sorted["Item-Total r"]],
        textposition="outside"
    ))
    fig.add_vline(x=0.3, line_dash="dash", line_color="#FF6B6B",
                  annotation_text="Min threshold (0.3)",
                  annotation_font_color="#FF6B6B")
    fig.update_layout(**CHART_LAYOUT, height=340,
                      title=dict(text="Item-Total Correlations",
                                 font=dict(color="#E8E8F0", family="Syne")))
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📋 Full item-total correlation table"):
    st.dataframe(itc, use_container_width=True)

# ── SECTION 2: Driver Rankings ─────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>2 · Driver Rankings by Mean Score</div>",
            unsafe_allow_html=True)

desc = ld.describe().T[["mean","std","50%"]].rename(
    columns={"mean":"Mean","std":"Std Dev","50%":"Median"})
desc["Rank"] = desc["Mean"].rank(ascending=False).astype(int)
desc["CV%"] = (desc["Std Dev"] / desc["Mean"] * 100).round(1)
ranking = desc.sort_values("Mean")

color_scale = [f"rgba(108,99,255,{0.4 + 0.6*i/len(ranking)})" for i in range(len(ranking))]

fig_rank = go.Figure(go.Bar(
    y=ranking.index, x=ranking["Mean"],
    orientation="h", marker_color=color_scale,
    error_x=dict(type="data", array=ranking["Std Dev"].values, color="#555577"),
    text=[f"μ={v:.2f}  #{int(r)}" for v, r in zip(ranking["Mean"], ranking["Rank"])],
    textposition="outside"
))
fig_rank.add_vline(x=3.0, line_dash="dash", line_color="#555577",
                   annotation_text="Neutral (3.0)", annotation_font_color="#9999BB")
fig_rank.add_vline(x=4.0, line_dash="dot", line_color="#6C63FF",
                   annotation_text="Agree (4.0)", annotation_font_color="#A89CFF")
fig_rank.update_layout(**CHART_LAYOUT, height=400,
                        xaxis=dict(range=[1, 5.8], gridcolor="rgba(255,255,255,0.06)"),
                        title=dict(text="Ranked Mean Scores of Adoption Drivers (±1 SD, n=228)",
                                   font=dict(color="#E8E8F0", family="Syne")))
st.plotly_chart(fig_rank, use_container_width=True)

# Stacked Likert chart
resp_labels = ["Strongly Disagree","Disagree","Neutral","Agree","Strongly Agree"]
resp_colors = ["#E53935","#EF9A9A","#FFF176","#A5D6A7","#2E7D32"]
pct_df = pd.DataFrame(index=SHORT_NAMES)
for val, lbl in zip([1,2,3,4,5], resp_labels):
    pct_df[lbl] = (ld == val).sum() / len(ld) * 100
pct_df["_pos"] = pct_df["Agree"] + pct_df["Strongly Agree"]
pct_df = pct_df.sort_values("_pos").drop(columns="_pos")

with st.expander("📊 Stacked Likert Response Distribution"):
    fig_stk = go.Figure()
    for lbl, color in zip(resp_labels, resp_colors):
        fig_stk.add_trace(go.Bar(
            name=lbl, y=pct_df.index, x=pct_df[lbl],
            orientation="h", marker_color=color,
            text=[f"{v:.0f}%" if v > 7 else "" for v in pct_df[lbl]],
            textposition="inside", insidetextanchor="middle"
        ))
    fig_stk.update_layout(barmode="stack", **CHART_LAYOUT, height=400,
                           xaxis=dict(title="% of Users", gridcolor="rgba(255,255,255,0.06)"),
                           legend=dict(orientation="h", y=-0.15,
                                       font=dict(color="#9999BB"), bgcolor="rgba(0,0,0,0)"),
                           title=dict(text="Stacked Likert Distributions",
                                      font=dict(color="#E8E8F0", family="Syne")))
    st.plotly_chart(fig_stk, use_container_width=True)

# ── SECTION 3: EFA ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>3 · Exploratory Factor Analysis (EFA)</div>",
            unsafe_allow_html=True)

ldf, communalities, eigenvalues, n_factors, pct_var = get_efa_results()

c1, c2 = st.columns(2)
with c1:
    # Scree plot
    fig_scree = go.Figure()
    fig_scree.add_trace(go.Scatter(
        x=list(range(1, len(eigenvalues)+1)), y=eigenvalues,
        mode="lines+markers", line=dict(color="#6C63FF", width=2.5),
        marker=dict(size=8, color="#6C63FF"),
        name="Eigenvalue"
    ))
    fig_scree.add_hline(y=1.0, line_dash="dash", line_color="#FF6B6B",
                         annotation_text="Kaiser criterion (EV=1)",
                         annotation_font_color="#FF6B6B")
    fig_scree.add_vrect(x0=0.5, x1=n_factors+0.5,
                         fillcolor="rgba(108,99,255,0.08)", line_width=0)
    for i in range(n_factors):
        fig_scree.add_annotation(x=i+1, y=eigenvalues[i]+0.15,
                                  text=f"F{i+1}<br>EV={eigenvalues[i]:.2f}",
                                  font=dict(size=9, color="#A89CFF"), showarrow=False)
    fig_scree.update_layout(**CHART_LAYOUT, height=340,
                             xaxis=dict(title="Factor Number", tickvals=list(range(1,11)),
                                        gridcolor="rgba(255,255,255,0.06)"),
                             yaxis=dict(title="Eigenvalue", gridcolor="rgba(255,255,255,0.06)"),
                             title=dict(text=f"Scree Plot — {n_factors} Factors Retained",
                                        font=dict(color="#E8E8F0", family="Syne")),
                             showlegend=False)
    st.plotly_chart(fig_scree, use_container_width=True)

with c2:
    # Communalities
    comm_colors = ["#FF6B6B" if h < 0.3 else "#FBBF24" if h < 0.6 else "#4ADE80"
                   for h in communalities]
    fig_comm = go.Figure(go.Bar(
        y=SHORT_NAMES, x=communalities,
        orientation="h", marker_color=comm_colors,
        text=[f"{v:.3f}" for v in communalities],
        textposition="outside"
    ))
    fig_comm.add_vline(x=0.3, line_dash="dash", line_color="#FF6B6B")
    fig_comm.update_layout(**CHART_LAYOUT, height=340,
                            xaxis=dict(title="Communality (h²)", range=[0, 1.1],
                                       gridcolor="rgba(255,255,255,0.06)"),
                            title=dict(text="Communalities (h²) per Item",
                                       font=dict(color="#E8E8F0", family="Syne")))
    st.plotly_chart(fig_comm, use_container_width=True)

# Factor loading heatmap
st.markdown("<div class='section-header' style='margin-top:12px;'>Rotated Factor Loading Matrix (Varimax)</div>",
            unsafe_allow_html=True)

plot_data = ldf.values
annot_text = [[f"{v:.3f}" if abs(v) >= 0.40 else f"<span style='opacity:0.3'>{v:.3f}</span>"
               for v in row] for row in plot_data]
annot_clean = [[f"{v:.3f}" for v in row] for row in plot_data]

fig_load = go.Figure(go.Heatmap(
    z=plot_data, x=ldf.columns.tolist(), y=SHORT_NAMES,
    colorscale=[
        [0, "#E53935"], [0.3, "#1A1A2E"], [0.5, "#1A1A2E"],
        [0.7, "#3D3580"], [1, "#6C63FF"]
    ],
    text=annot_clean, texttemplate="%{text}", textfont=dict(size=11, color="#E8E8F0"),
    zmid=0, zmin=-1, zmax=1,
    colorbar=dict(title="Loading", tickfont=dict(color="#9999BB"))
))
fig_load.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=380, margin=dict(t=20, b=20, l=10, r=10),
                        font=dict(color="#9999BB", family="DM Sans"),
                        title=dict(text=f"Factor Loadings — {pct_var.sum():.1f}% total variance explained (|loading| ≥ 0.40 = meaningful)",
                                   font=dict(color="#E8E8F0", family="Syne", size=12)))
st.plotly_chart(fig_load, use_container_width=True)

with st.expander("📋 Factor loading details & variance explained"):
    st.dataframe(ldf.round(3), use_container_width=True)
    st.markdown(f"**Variance explained per factor:** " +
                " | ".join([f"F{i+1}: {v:.1f}%" for i, v in enumerate(pct_var)]))
    st.markdown(f"**Total variance explained:** {pct_var.sum():.1f}%")
    st.markdown(f"**Number of factors retained (Kaiser criterion, EV > 1):** {n_factors}")

# ── SECTION 4: Non-User Barriers ───────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>4 · Non-User Barrier Analysis (n=113)</div>",
            unsafe_allow_html=True)

BARRIER_COLS = [
    "I would consider using Q-commerce if delivery charges were lower",
    "I would consider using Q-commerce apps if product quality were guaranteed",
    "I would consider using Q-commerce apps if adequate guidance on app usage were provided",
    "I would consider using Q-commerce apps if prices were competitive",
    "I would consider using Q-commerce apps if delivery services were available in my area",
    "I would consider using Q-commerce apps if attractive discounts were offered",
    "I would consider using Q-commerce apps if I felt confident about trust, data security, and privacy."
]
BARRIER_NAMES = ["Lower Delivery Charges","Product Quality Guarantee","App Usage Guidance",
                 "Competitive Pricing","Delivery Availability","Attractive Discounts",
                 "Trust & Data Security"]

bd = non_users[BARRIER_COLS].copy()
for col in BARRIER_COLS:
    bd[col] = bd[col].map(LIKERT_MAP)
bd.columns = BARRIER_NAMES
bd = bd.dropna()

b_desc = bd.describe().T[["mean","std"]].rename(columns={"mean":"Mean","std":"Std Dev"})
b_desc["Rank"] = b_desc["Mean"].rank(ascending=False).astype(int)
b_sorted = b_desc.sort_values("Mean")

bar_colors = [f"rgba(255,107,107,{0.4 + 0.6*i/len(b_sorted)})" for i in range(len(b_sorted))]

fig_bar = go.Figure(go.Bar(
    y=b_sorted.index, x=b_sorted["Mean"],
    orientation="h", marker_color=bar_colors,
    error_x=dict(type="data", array=b_sorted["Std Dev"].values, color="#555577"),
    text=[f"μ={v:.2f}  #{int(r)}" for v, r in zip(b_sorted["Mean"], b_sorted["Rank"])],
    textposition="outside"
))
fig_bar.add_vline(x=3.0, line_dash="dash", line_color="#555577",
                  annotation_text="Neutral (3.0)", annotation_font_color="#9999BB")
fig_bar.add_vline(x=4.0, line_dash="dot", line_color="#FF6B6B",
                  annotation_text="Agree (4.0)", annotation_font_color="#FF6B6B")
fig_bar.update_layout(**CHART_LAYOUT, height=360,
                       xaxis=dict(range=[1,5.8], gridcolor="rgba(255,255,255,0.06)"),
                       title=dict(text="Barriers to Adoption — Non-Users (higher = stronger barrier)",
                                  font=dict(color="#E8E8F0", family="Syne")))
st.plotly_chart(fig_bar, use_container_width=True)

# Open-ended reasons
reason_cols = [c for c in non_users.columns if "usex" in c.lower()]
reason_raw = []
for col in reason_cols:
    reason_raw.extend(non_users[col].dropna().astype(str).str.strip().tolist())

reason_map = {
    "Delivery charges are high": "High Delivery Charges",
    " Product quality concerns": "Product Quality Concerns",
    "Product quality concerns": "Product Quality Concerns",
    " No need for fast delivery": "No Need for Fast Delivery",
    "I prefer buying from local stores": "Prefer Local Stores",
    " Do no trust online delivery": "Do Not Trust Online Delivery",
    "Do no trust online delivery": "Do Not Trust Online Delivery",
    " Not comfortable using apps": "Not Comfortable Using Apps",
    "Not comfortable using apps": "Not Comfortable Using Apps",
    "Not aware how to use the apps": "Unaware How to Use Apps",
    " Not aware how to use the apps": "Unaware How to Use Apps",
    " Payment safety concerns": "Payment Safety Concerns",
    "Payment safety concerns": "Payment Safety Concerns",
}
reasons = pd.Series(reason_raw).str.strip().replace(reason_map).value_counts()
reasons = reasons[reasons.index.str.len() > 2]

fig_reasons = go.Figure(go.Bar(
    y=reasons.index[::-1], x=reasons.values[::-1],
    orientation="h", marker_color="#FF6B6B",
    text=[f"n={v} ({v/len(non_users)*100:.1f}%)" for v in reasons.values[::-1]],
    textposition="outside"
))
fig_reasons.update_layout(**CHART_LAYOUT, height=340,
                           xaxis=dict(title="Number of Non-Users", gridcolor="rgba(255,255,255,0.06)"),
                           title=dict(text="Open-Ended Barriers Cited by Non-Users",
                                      font=dict(color="#E8E8F0", family="Syne")))
st.plotly_chart(fig_reasons, use_container_width=True)

# ── Key Findings ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>Key Findings — Objective 4</div>", unsafe_allow_html=True)

findings = [
    ("🔬 Strong Scale Reliability",
     f"Cronbach's α = {alpha:.3f} — the 10-item attitude scale shows {interp.replace(' ✦','')} internal consistency, validating all subsequent factor analyses."),
    ("⚡ Convenience Tops the Rankings",
     "Time Saving, Delivery Speed, and Lifestyle Fit consistently score near or above the Agree threshold (≥4.0), making convenience the primary adoption motivator."),
    ("🎯 EFA Reveals Latent Structure",
     f"{n_factors} factors retained (Kaiser criterion). After Varimax rotation, items separate into distinct dimensions — convenience/lifestyle, price sensitivity, and reliability/trust — revealing adoption is multi-dimensional."),
    ("🚧 Trust & Cost Block Non-Users",
     "Among 113 non-users, 'Trust & Data Security' and 'Lower Delivery Charges' score highest as would-be adoption triggers. 'Prefer Local Stores' and 'Unaware How to Use Apps' are the most cited open-ended barriers — behavioral inertia and digital literacy gaps."),
]
for title, text in findings:
    st.markdown(f"""
    <div class='finding-card'>
        <h4>{title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)
