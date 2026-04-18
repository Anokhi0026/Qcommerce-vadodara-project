import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
from data_loader import (load_data, get_product_categories, get_kruskal_results,
                          get_spearman_corr, run_chi_square,
                          AGE_ORDER, TENURE_ORDER, ORDER_ORDER, TIME_ORDER,
                          PAY_ORDER, APP_ORDER, INCOME_ORDER)

st.set_page_config(page_title="Obj 3 — Usage Behavior", page_icon="📊",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; font-weight:700 !important; }
.section-header {
    font-family:'Syne',sans-serif; font-size:0.72rem; font-weight:600;
    color:#6C63FF; text-transform:uppercase; letter-spacing:0.15em; margin-bottom:6px;
}
.finding-card {
    background:#1A1A2E; border-left:3px solid #6C63FF;
    border-radius:0 12px 12px 0; padding:16px 20px; margin:10px 0;
}
.finding-card h4 { font-family:'Syne',sans-serif !important; font-size:0.95rem !important;
    color:#E8E8F0 !important; margin:0 0 6px 0 !important; }
.finding-card p { font-size:0.85rem; color:#9999BB; margin:0; line-height:1.6; }
.stat-pill {
    display:inline-block; background:rgba(108,99,255,0.15);
    border:1px solid rgba(108,99,255,0.3); color:#A89CFF;
    border-radius:20px; padding:3px 10px; font-size:0.78rem; margin:2px;
}
.sig-yes { color:#4ADE80; font-weight:600; }
.sig-no  { color:#9999BB; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px;'>
        <div style='font-family:Syne,sans-serif; font-size:1.3rem; font-weight:800; color:#E8E8F0;'>⚡ Q-Commerce</div>
        <div style='font-size:0.75rem; color:#9999BB; margin-top:4px;'>Vadodara Research Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                    label="🏠  Overview")
    st.page_link("pages/1_Objective_3.py",    label="📊  Obj 3 — Usage Behavior")
    st.page_link("pages/2_Objective_4.py",    label="🔍  Obj 4 — Key Drivers")
    st.page_link("pages/3_Objective_5.py",    label="🤖  Obj 5 — Predictive Models")
    st.page_link("pages/4_About.py",          label="ℹ️   About & Methods")

df, users, non_users = load_data()

st.markdown("""
<span style='font-family:Syne,sans-serif; font-size:0.75rem; color:#6C63FF;
             text-transform:uppercase; letter-spacing:0.12em;'>Objective 3</span>
<h1 style='font-family:Syne,sans-serif; font-size:2.1rem; font-weight:800;
           color:#E8E8F0; margin:4px 0 8px;'>Usage Behavior Patterns</h1>
<p style='color:#9999BB; max-width:680px; line-height:1.7; font-size:0.95rem;'>
Examining frequency, order size, preferred delivery times, payment methods,
and satisfaction scores among <b style='color:#A89CFF;'>228 active Q-Commerce users</b> in Vadodara.
</p>
""", unsafe_allow_html=True)

# ── SECTION 1: Descriptive Profiles ───────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>1 · Descriptive Profile</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📱 App & Tenure", "💸 Spending & Payment", "📦 Products & Timing"])

COLORS = ["#6C63FF", "#FF6B6B", "#4ADE80", "#FBBF24", "#38BDF8", "#F472B6"]
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#9999BB", family="DM Sans"),
    margin=dict(t=30, b=10, l=10, r=10),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)")
)

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        app_counts = users["App_Used"].value_counts().reindex(APP_ORDER).fillna(0)
        fig = go.Figure(go.Bar(
            x=app_counts.index, y=app_counts.values,
            marker_color=COLORS[:len(app_counts)],
            text=[f"{v:.0f}<br>({v/app_counts.sum()*100:.1f}%)" for v in app_counts.values],
            textposition="outside", textfont=dict(size=11)
        ))
        fig.update_layout(**CHART_LAYOUT, height=320,
                          title=dict(text="Primary App Used", font=dict(color="#E8E8F0", family="Syne")))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        tenure_col = "How long have you been using Q-Commerce apps?"
        ten = users[tenure_col].value_counts().reindex(TENURE_ORDER).fillna(0)
        fig = go.Figure(go.Bar(
            x=ten.index, y=ten.values,
            marker_color=COLORS[:len(ten)],
            text=[f"{v:.0f}<br>({v/ten.sum()*100:.1f}%)" for v in ten.values],
            textposition="outside", textfont=dict(size=11)
        ))
        fig.update_layout(**CHART_LAYOUT, height=320,
                          title=dict(text="Usage Tenure", font=dict(color="#E8E8F0", family="Syne")))
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Detailed frequency tables"):
        c1, c2 = st.columns(2)
        with c1:
            t = pd.DataFrame({"Count": app_counts.values,
                               "%": (app_counts.values / app_counts.sum() * 100).round(1)},
                              index=app_counts.index)
            st.dataframe(t, use_container_width=True)
        with c2:
            t2 = pd.DataFrame({"Count": ten.values,
                                "%": (ten.values / ten.sum() * 100).round(1)},
                               index=ten.index)
            st.dataframe(t2, use_container_width=True)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        ord_counts = users["average order value"].value_counts().reindex(ORDER_ORDER).fillna(0)
        fig = go.Figure(go.Bar(
            x=ord_counts.index, y=ord_counts.values,
            marker_color=COLORS[:len(ord_counts)],
            text=[f"{v:.0f} ({v/ord_counts.sum()*100:.1f}%)" for v in ord_counts.values],
            textposition="outside", textfont=dict(size=11)
        ))
        fig.update_layout(**CHART_LAYOUT, height=320,
                          title=dict(text="Average Order Value", font=dict(color="#E8E8F0", family="Syne")))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        pay_counts = users["preferred payment method?"].value_counts().reindex(PAY_ORDER).fillna(0)
        fig = go.Figure(go.Pie(
            labels=pay_counts.index, values=pay_counts.values,
            hole=0.5, marker_colors=COLORS,
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=11, color="#E8E8F0")
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", showlegend=False,
                          height=320, margin=dict(t=30, b=10, l=10, r=10),
                          title=dict(text="Payment Method", font=dict(color="#E8E8F0", family="Syne")))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        time_counts = users["preferred delivery time"].value_counts().reindex(TIME_ORDER).fillna(0)
        fig = go.Figure(go.Bar(
            y=time_counts.index[::-1], x=time_counts.values[::-1],
            orientation="h", marker_color=COLORS[:len(time_counts)],
            text=[f"{v:.0f} ({v/time_counts.sum()*100:.1f}%)" for v in time_counts.values[::-1]],
            textposition="outside"
        ))
        fig.update_layout(**CHART_LAYOUT, height=320,
                          title=dict(text="Preferred Delivery Time", font=dict(color="#E8E8F0", family="Syne")))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        cat_series = get_product_categories()
        fig = go.Figure(go.Bar(
            y=cat_series.index[::-1], x=cat_series.values[::-1],
            orientation="h", marker_color=COLORS[:len(cat_series)],
            text=[f"{v} ({v/len(users)*100:.1f}%)" for v in cat_series.values[::-1]],
            textposition="outside"
        ))
        fig.update_layout(
            height=320,
            xaxis=dict(title="No. of Users", gridcolor="rgba(255,255,255,0.06)"),
            title=dict(
                text="Products Ordered (Multi-response, n=228)",
                font=dict(color="#E8E8F0", family="Syne")
            )
        )

# ── SECTION 2: Chi-Square Tests ────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>2 · Chi-Square Tests — Behavior vs Demographics</div>",
            unsafe_allow_html=True)
st.markdown("""
<p style='color:#9999BB; font-size:0.88rem;'>
H₀: The behavioral variable is independent of the demographic variable. (α = 0.05)
</p>
""", unsafe_allow_html=True)

behavior_map = {
    "App_Used": "App Used",
    "How long have you been using Q-Commerce apps?": "Usage Tenure",
    "average order value": "Avg. Order Value",
    "preferred delivery time": "Preferred Delivery Time",
    "preferred payment method?": "Payment Method"
}
demo_map = {
    "Age_Group": "Age Group",
    "Income": "Income",
    "Occupation": "Occupation",
    "Education": "Education"
}

rows = []
for bcol, blabel in behavior_map.items():
    for dcol, dlabel in demo_map.items():
        try:
            r = run_chi_square(bcol, dcol)
            assoc_color = {"Negligible": "#4A4A6A", "Weak": "#9999BB",
                           "Moderate": "#FBBF24", "Strong": "#4ADE80"}.get(r["assoc"], "#9999BB")
            rows.append({"Behavior": blabel, "Demographic": dlabel,
                         "χ²": round(r["chi2"], 3), "df": r["dof"],
                         "p-value": round(r["p"], 4),
                         "Cramér's V": round(r["v"], 3),
                         "Association": r["assoc"],
                         "Significant": "✓ Yes" if r["sig"] else "✗ No"})
        except:
            pass

chi_df = pd.DataFrame(rows)

# Heatmap of Cramér's V
pivot = chi_df.pivot_table(index="Behavior", columns="Demographic", values="Cramér's V")
pivot_p = chi_df.pivot_table(index="Behavior", columns="Demographic", values="p-value")

annots = [[f"{pivot.iloc[r, c]:.2f}{'**' if pivot_p.loc[r,c]<0.01 else '*' if pivot_p.loc[r,c]<0.05 else ''}"
           for c in pivot.columns] for r in pivot.index]

fig_hm = go.Figure(go.Heatmap(
    z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
    colorscale=[[0, "#1A1A2E"], [0.3, "#3D3580"], [0.6, "#6C63FF"], [1, "#A89CFF"]],
    text=annots, texttemplate="%{text}", textfont=dict(size=12, color="#E8E8F0"),
    colorbar=dict(title="V", tickfont=dict(color="#9999BB")),
    zmin=0, zmax=0.6
))
fig_hm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=340, margin=dict(t=30, b=10, l=10, r=10),
                      font=dict(color="#9999BB", family="DM Sans"),
                      title=dict(text="Cramér's V Heatmap (** p<0.01, * p<0.05)",
                                 font=dict(color="#E8E8F0", family="Syne")))
st.plotly_chart(fig_hm, use_container_width=True)

with st.expander("📋 Full chi-square results table"):
    st.dataframe(chi_df.style.applymap(
        lambda v: "color: #4ADE80; font-weight:600" if v == "✓ Yes" else "color: #9999BB",
        subset=["Significant"]
    ), use_container_width=True)

    sig_df = chi_df[chi_df["Significant"] == "✓ Yes"].sort_values("Cramér's V", ascending=False)
    if not sig_df.empty:
        st.markdown("**Significant associations found:**")
        for _, row in sig_df.iterrows():
            st.markdown(f"""
            <div class='finding-card'>
                <h4>{row['Behavior']} × {row['Demographic']}</h4>
                <p>χ²={row['χ²']}, p={row['p-value']}, Cramér's V={row["Cramér's V"]}
                ({row['Association']} association)</p>
            </div>
            """, unsafe_allow_html=True)

# ── SECTION 3: Satisfaction Analysis ──────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>3 · Satisfaction Analysis</div>", unsafe_allow_html=True)

sat_col  = "Overall satisfaction with Q-Commerce Apps"
cont_col = "Likelihood of continuing usage in the future"
rec_col  = "likely are you to recommend these apps to Others"
sat_vars = [sat_col, cont_col, rec_col]
sat_labels = ["Overall Satisfaction", "Continuity Likelihood", "Recommendation Likelihood"]

c1, c2, c3 = st.columns(3)
for col, sc, sl in zip([c1, c2, c3], sat_vars, sat_labels):
    with col:
        data = users[sc].dropna()
        col.metric(sl, f"{data.mean():.2f} / 5",
                   f"Median: {data.median():.0f} | SD: {data.std():.2f}")

# Distribution
fig_dist = go.Figure()
for sc, sl, color in zip(sat_vars, sat_labels, COLORS):
    data = users[sc].dropna()
    counts = data.value_counts().sort_index()
    fig_dist.add_trace(go.Bar(name=sl, x=counts.index, y=counts.values,
                               marker_color=color, opacity=0.85))
fig_dist.update_layout(**CHART_LAYOUT, barmode="group", height=320,
                        title=dict(text="Satisfaction Score Distributions (1–5 scale)",
                                   font=dict(color="#E8E8F0", family="Syne")),
                        legend=dict(font=dict(color="#9999BB"), bgcolor="rgba(0,0,0,0)"),
                        xaxis=dict(tickvals=[1,2,3,4,5], gridcolor="rgba(255,255,255,0.06)"))
st.plotly_chart(fig_dist, use_container_width=True)

# Spearman correlation heatmap
corr_df, pval_df = get_spearman_corr()
labels = ["Satisfaction", "Continuity", "Recommendation"]

annot_corr = [[f"ρ={corr_df.iloc[i,j]:.3f}<br>p={pval_df.iloc[i,j]:.3f}" if i != j else "—"
               for j in range(3)] for i in range(3)]

fig_corr = go.Figure(go.Heatmap(
    z=corr_df.values, x=labels, y=labels,
    colorscale=[[0, "#1A1A2E"], [0.5, "#3D3580"], [1, "#6C63FF"]],
    text=annot_corr, texttemplate="%{text}", textfont=dict(size=11, color="#E8E8F0"),
    zmin=0, zmax=1,
    colorbar=dict(title="ρ", tickfont=dict(color="#9999BB"))
))
fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=300, margin=dict(t=30, b=10, l=10, r=10),
                        font=dict(color="#9999BB", family="DM Sans"),
                        title=dict(text="Spearman Correlation Matrix",
                                   font=dict(color="#E8E8F0", family="Syne")))
st.plotly_chart(fig_corr, use_container_width=True)

# Kruskal-Wallis
kw_df = get_kruskal_results()
with st.expander("📊 Kruskal-Wallis H Test Results — Satisfaction by Demographics"):
    st.markdown("""
    <p style='color:#9999BB; font-size:0.85rem;'>
    H₀: Median satisfaction is equal across groups. Non-parametric ANOVA for ordinal data.
    </p>
    """, unsafe_allow_html=True)
    for score in kw_df["Score"].unique():
        sub = kw_df[kw_df["Score"] == score]
        st.markdown(f"**{score}**")
        st.dataframe(sub[["Group By","H","p","Significant"]].reset_index(drop=True),
                     use_container_width=True)

# ── Key Findings ───────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("<div class='section-header'>Key Findings — Objective 3</div>",
            unsafe_allow_html=True)

findings = [
    ("🏆 Blinkit Dominates",
     "~62% of Q-Commerce users in Vadodara primarily use Blinkit, reflecting near-oligopolistic market structure. Only 16% are very recent users (< 3 months), confirming Q-Commerce has crossed from trial to mainstream habitual use."),
    ("🌙 Evening Orders Peak",
     "Evening (40%) and Night (23%) together account for 63% of all orders — users place orders after returning home when they realize a need, not during the day. Younger users (18–33) are more active at night."),
    ("💳 UPI Rules, CoD Persists",
     "UPI dominates at ~54%, but Cash on Delivery at ~32% signals residual hesitancy about digital payments among a meaningful segment — an adoption gap for platforms to address."),
    ("📦 Groceries & Essentials Dominate",
     "Groceries (72.8%), Snacks (63.6%), and Daily Essentials (56.6%) are top categories — Q-Commerce is positioned as a daily-replenishment service, not a specialty platform."),
    ("💛 Satisfaction is High & Correlated",
     "Mean satisfaction = 3.82/5. The strong Spearman correlations between satisfaction, continuity, and recommendation scores confirm the satisfaction-loyalty-advocacy chain in Q-Commerce."),
]
for title, text in findings:
    st.markdown(f"""
    <div class='finding-card'>
        <h4>{title}</h4>
        <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)
