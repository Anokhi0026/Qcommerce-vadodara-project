import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, kruskal, spearmanr, mannwhitneyu
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

LIKERT_MAP = {
    "Strongly Disagree": 1, "Disagree": 2,
    "Neutral": 3, "Agree": 4, "Strongly Agree": 5
}

LIKERT_COLS = [
    "Q-commerce apps save my time",
    "Delivery speed is very convenient",
    "Discounts influence my usage",
    "Product variety meets my needs",
    "Promotional offers attract me",
    "Apps are easy to navigate",
    "Urgent needs motivate me to use these apps",
    "Product quality is reliable",
    "My work/study schedule makes offline shopping difficult",
    "Q-commerce fits my lifestyle"
]

SHORT_NAMES = [
    "Time Saving", "Delivery Speed", "Discounts", "Product Variety",
    "Promo Offers", "Ease of Use", "Urgent Needs", "Quality Reliable",
    "Schedule Barrier", "Lifestyle Fit"
]

AGE_ORDER    = ["18-25", "26-33", "34-41", "42-49", "50 or above"]
TENURE_ORDER = ["Less than 3 months", "3-6 months", "6-12 months", "More than a year"]
ORDER_ORDER  = ["Below ₹200", "₹200 - ₹400", "₹400 - ₹600", "Above ₹600"]
TIME_ORDER   = ["Morning", "Afternoon", "Evening", "Night", "Midnight"]
PAY_ORDER    = ["UPI", "Cash on Delivery", "Debit/Credit Card", "Wallets (Paytm, PhonePe, etc.)"]
APP_ORDER    = ["Blinkit", "Swiggy Instamart", "Zepto", "Other"]
INCOME_ORDER = ["Below ₹20,000", "₹20,000 - ₹40,000", "₹40,000 - ₹60,000",
                "₹60,000 - ₹1,00,000", "Above ₹1,00,000"]

import streamlit as st

@st.cache_data
def load_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "me.xlsx")

    df = pd.read_excel(file_path, sheet_name="raw", header=1)
    users = df[df["Adoption_Status"] == 1].copy().reset_index(drop=True)
    non_users = df[df["Adoption_Status"] == 0].copy().reset_index(drop=True)
    return df, users, non_users

@st.cache_data
def get_likert_data():
    _, users, _ = load_data()
    ld = users[LIKERT_COLS].copy()
    for col in LIKERT_COLS:
        ld[col] = ld[col].map(LIKERT_MAP)
    ld.columns = SHORT_NAMES
    return ld.dropna()

@st.cache_data
def cramers_v(chi2_val, n, r, c):
    phi2 = chi2_val / n
    phi2corr = max(0, phi2 - ((c - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    ccorr = c - ((c - 1) ** 2) / (n - 1)
    denom = min(rcorr - 1, ccorr - 1)
    if denom <= 0:
        return phi2corr
    return np.sqrt(phi2corr / denom)

@st.cache_data
def run_chi_square(behavior_col, demo_col):
    _, users, _ = load_data()
    ct = pd.crosstab(users[behavior_col], users[demo_col])
    chi2, p, dof, _ = chi2_contingency(ct)
    n = ct.values.sum()
    r, c = ct.shape
    v = cramers_v(chi2, n, r, c)
    assoc = ("Negligible" if v < 0.1 else "Weak" if v < 0.3
             else "Moderate" if v < 0.5 else "Strong")
    return {"chi2": chi2, "p": p, "dof": dof, "v": v, "assoc": assoc,
            "sig": p < 0.05, "crosstab": ct}

@st.cache_data
def cronbach_alpha(data_tuple):
    df = pd.DataFrame(list(data_tuple))
    k = df.shape[1]
    item_var = df.var(axis=0, ddof=1).sum()
    total_var = df.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_var / total_var)

@st.cache_data
def get_item_total_corr():
    ld = get_likert_data()
    results = []
    total = ld.sum(axis=1)
    for col in ld.columns:
        corrected = total - ld[col]
        r, _ = stats.pearsonr(ld[col], corrected)
        alpha_del = cronbach_alpha(tuple(map(tuple, ld.drop(columns=[col]).values)))
        results.append({"Item": col, "Mean": round(ld[col].mean(), 3),
                        "SD": round(ld[col].std(), 3),
                        "Item-Total r": round(r, 3),
                        "Alpha if Deleted": round(alpha_del, 3)})
    return pd.DataFrame(results)

@st.cache_data
def get_product_categories():
    _, users, _ = load_data()
    cat_cols = ["Col1", "Col2", "Col3", "Col4", "Col5"]
    all_cats = []
    for col in cat_cols:
        all_cats.extend(users[col].dropna().str.strip().tolist())
    counts = {}
    for k in all_cats:
        key = k.strip()
        counts[key] = counts.get(key, 0) + 1
    return pd.Series(counts).sort_values(ascending=False)

@st.cache_data
def get_kruskal_results():
    _, users, _ = load_data()
    sat_col  = "Overall satisfaction with Q-Commerce Apps"
    cont_col = "Likelihood of continuing usage in the future"
    rec_col  = "likely are you to recommend these apps to Others"
    sat_vars = [sat_col, cont_col, rec_col]
    sat_labels = ["Overall Satisfaction", "Continuity Likelihood", "Recommendation Likelihood"]
    group_vars = ["Age_Group", "Income", "Occupation", "App_Used"]
    results = []
    for gv in group_vars:
        for sv, sl in zip(sat_vars, sat_labels):
            groups = [g[sv].dropna().values for _, g in users.groupby(gv)
                      if len(g[sv].dropna()) >= 3]
            if len(groups) >= 2:
                H, p = kruskal(*groups)
                results.append({"Score": sl, "Group By": gv,
                                 "H": round(H, 3), "p": round(p, 4),
                                 "Significant": p < 0.05})
    return pd.DataFrame(results)

@st.cache_data
def get_spearman_corr():
    _, users, _ = load_data()
    sat_col  = "Overall satisfaction with Q-Commerce Apps"
    cont_col = "Likelihood of continuing usage in the future"
    rec_col  = "likely are you to recommend these apps to Others"
    sat_vars = [sat_col, cont_col, rec_col]
    labels   = ["Satisfaction", "Continuity", "Recommendation"]
    data = users[sat_vars].dropna()
    corr = np.zeros((3, 3))
    pval = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            if i == j:
                corr[i, j] = 1.0
            else:
                r, p = spearmanr(data.iloc[:, i], data.iloc[:, j])
                corr[i, j] = r
                pval[i, j] = p
    return pd.DataFrame(corr, index=labels, columns=labels), \
           pd.DataFrame(pval, index=labels, columns=labels)

@st.cache_data
def get_efa_results():
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    ld = get_likert_data()
    X = ld.values.astype(float)
    X_std = StandardScaler().fit_transform(X)
    corr_mat = np.corrcoef(X_std.T)
    eigenvalues, _ = np.linalg.eigh(corr_mat)
    eigenvalues = eigenvalues[::-1]
    n_factors = int((eigenvalues > 1).sum())
    pca = PCA(n_components=n_factors)
    pca.fit(X_std)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

    def varimax(L, max_iter=1000, tol=1e-6):
        p, k = L.shape
        R = np.eye(k)
        for _ in range(max_iter):
            old = R.copy()
            for i in range(k):
                for j in range(i + 1, k):
                    Lr = L @ R
                    Li, Lj = Lr[:, i], Lr[:, j]
                    u = Li**2 - Lj**2
                    v = 2 * Li * Lj
                    A, B = np.sum(u), np.sum(v)
                    C = np.sum(u**2 - v**2)
                    D = 2 * np.sum(u * v)
                    theta = 0.25 * np.arctan2(D - 2*A*B/p, C - (A**2 - B**2)/p)
                    c, s = np.cos(theta), np.sin(theta)
                    G = np.eye(k)
                    G[i, i] = c; G[j, j] = c
                    G[i, j] = -s; G[j, i] = s
                    R = R @ G
            if np.max(np.abs(R - old)) < tol:
                break
        return L @ R

    rot = varimax(loadings)
    factor_cols = [f"Factor {i+1}" for i in range(n_factors)]
    ldf = pd.DataFrame(rot, index=SHORT_NAMES, columns=factor_cols)
    communalities = np.sum(rot**2, axis=1)
    ssl = np.sum(rot**2, axis=0)
    pct_var = ssl / 10 * 100
    return ldf, communalities, eigenvalues, n_factors, pct_var

@st.cache_data
def get_logistic_results():
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score, roc_curve
    from sklearn.model_selection import StratifiedKFold, cross_val_score
    df, _, _ = load_data()

    gender_d = pd.get_dummies(df["Gender"], prefix="Gender")
    age_d    = pd.get_dummies(df["Age_Group"], prefix="Age")
    edu_d    = pd.get_dummies(df["Education"], prefix="Edu")
    occ_d    = pd.get_dummies(df["Occupation"], prefix="Occ")
    inc_d    = pd.get_dummies(df["Income"], prefix="Inc")

    for col, dd in [("Gender_Male", gender_d), ("Age_18-25", age_d),
                    ("Edu_School Level", edu_d), ("Occ_Student", occ_d),
                    ("Inc_Below ₹20,000", inc_d)]:
        if col in dd.columns:
            dd.drop(columns=[col], inplace=True)

    X = pd.concat([gender_d, age_d, edu_d, occ_d, inc_d], axis=1).astype(float)
    y = df["Adoption_Status"].astype(float)
    mask = X.notna().all(axis=1) & y.notna()
    X, y = X[mask], y[mask]

    model = LogisticRegression(C=1000, solver="lbfgs", max_iter=2000, random_state=42)
    model.fit(X, y)

    np.random.seed(42)
    n_boot = 300
    boot_coefs = np.zeros((n_boot, len(model.coef_[0])))
    for b in range(n_boot):
        idx = np.random.choice(len(y), len(y), replace=True)
        m = LogisticRegression(C=1000, solver="lbfgs", max_iter=2000)
        m.fit(X.values[idx], y.values[idx])
        boot_coefs[b] = m.coef_[0]

    coefs = model.coef_[0]
    or_vals = np.exp(coefs)
    ci_lo = np.exp(np.percentile(boot_coefs, 2.5, axis=0))
    ci_hi = np.exp(np.percentile(boot_coefs, 97.5, axis=0))
    sig = ["Yes" if not (lo <= 1 <= hi) else "No"
           for lo, hi in zip(ci_lo, ci_hi)]

    coef_df = pd.DataFrame({
        "Predictor": X.columns,
        "β": coefs.round(3),
        "OR": or_vals.round(3),
        "CI_lo": ci_lo.round(3),
        "CI_hi": ci_hi.round(3),
        "Significant": sig
    }).sort_values("OR", ascending=False)

    y_prob = model.predict_proba(X)[:, 1]
    auc = roc_auc_score(y, y_prob)
    fpr, tpr, thr = roc_curve(y, y_prob)
    cv_auc = cross_val_score(model, X, y,
                              cv=StratifiedKFold(5, shuffle=True, random_state=42),
                              scoring="roc_auc").mean()
    n = len(y)
    p_bar = y.mean()
    ll_null = n * (p_bar * np.log(p_bar) + (1 - p_bar) * np.log(1 - p_bar))
    ll_mod  = np.sum(y.values * np.log(np.clip(y_prob, 1e-10, 1 - 1e-10)) +
                     (1 - y.values) * np.log(np.clip(1 - y_prob, 1e-10, 1 - 1e-10)))
    cs  = 1 - np.exp(-2 * (ll_mod - ll_null) / n)
    nag = cs / (1 - np.exp(2 * ll_null / n))

    j = tpr - fpr
    opt = np.argmax(j)

    return coef_df, auc, cv_auc, nag, fpr, tpr, thr[opt]

@st.cache_data
def get_mannwhitney_results():
    df, _, _ = load_data()
    df = df.copy()
    AGE_ORD    = {"18-25": 1, "26-33": 2, "34-41": 3, "42-49": 4, "50 or above": 5}
    EDU_ORD    = {"No Formal Education": 1, "School Level": 2,
                  "Undergraduate": 3, "Postgraduate": 4, "Professional Degree": 5}
    INC_ORD    = {"Below ₹20,000": 1, "₹20,000 - ₹40,000": 2,
                  "₹40,000 - ₹60,000": 3, "₹60,000 - ₹1,00,000": 4, "Above ₹1,00,000": 5}
    df["Age_Ord"] = df["Age_Group"].map(AGE_ORD)
    df["Edu_Ord"] = df["Education"].map(EDU_ORD)
    df["Inc_Ord"] = df["Income"].map(INC_ORD)

    results = []
    for var, col in [("Age", "Age_Ord"), ("Education", "Edu_Ord"), ("Income", "Inc_Ord")]:
        u_d  = df[df["Adoption_Status"] == 1][col].dropna()
        nu_d = df[df["Adoption_Status"] == 0][col].dropna()
        U, p = mannwhitneyu(u_d, nu_d, alternative="two-sided")
        rb = 1 - (2 * U) / (len(u_d) * len(nu_d))
        eff = "Large" if abs(rb) > 0.5 else "Medium" if abs(rb) > 0.3 else "Small"
        results.append({"Variable": var,
                         "Users Median": u_d.median(),
                         "Non-Users Median": nu_d.median(),
                         "U": round(U, 1), "p": round(p, 4),
                         "r": round(rb, 3), "Effect": eff,
                         "Significant": p < 0.05})
    return pd.DataFrame(results)

