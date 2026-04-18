# ⚡ Q-Commerce Vadodara — Research Dashboard

> **A Study on Consumer Usage and Adoption of Q-Commerce Applications in Vadodara**  
> MSc Statistics · The Maharaja Sayajirao University of Baroda · 2024–25

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

---

## 📋 About

An interactive statistical research dashboard built with **Streamlit** and **Plotly**, presenting a complete analysis of Q-Commerce (quick-delivery app) usage and adoption patterns among 341 consumers in Vadodara, Gujarat.

**Sample:** 341 respondents — 228 active users + 113 non-users  
**Data collection:** Google Forms structured questionnaire (8 pages)  
**Apps studied:** Blinkit, Zepto, Swiggy Instamart

---

## 🗂️ Dashboard Pages

| Page | Content |
|------|---------|
| 🏠 **Overview** | KPI cards, sample composition, headline findings |
| 📊 **Objective 3** | Usage behavior — apps, tenure, spending, delivery time, satisfaction |
| 🔍 **Objective 4** | Key drivers — Cronbach's α, EFA, factor loadings, non-user barriers |
| 🤖 **Objective 5** | Predictive models — logistic regression, ROC/AUC, odds ratios |
| ℹ️ **About** | Study details, all 23 statistical tests, tech stack |

---

## 📊 Statistical Methods (23 Tests)

- Chi-Square Test of Independence + Cramér's V
- Kruskal-Wallis H Test + Dunn's Post-Hoc (Bonferroni)
- Spearman Rank Correlation
- Cronbach's Alpha + Item-Total Correlations
- KMO Test + Bartlett's Test of Sphericity
- Exploratory Factor Analysis (PCA + Varimax Rotation)
- Mann-Whitney U Test + Rank-Biserial r
- Binary Logistic Regression (Model 1 + Model 2)
- Bootstrap 95% Confidence Intervals (300 resamples)
- Nagelkerke Pseudo-R² + ROC/AUC
- Youden's J Optimal Threshold
- Stratified 5-Fold Cross-Validated AUC

---

## 🚀 Deployment Guide — GitHub + Streamlit Cloud

### Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click **"+"** → **"New repository"**
3. Name it: `qcommerce-vadodara-dashboard`
4. Set to **Public**
5. Do NOT initialize with README (you already have one)
6. Click **"Create repository"**

### Step 2: Upload Files to GitHub

You have two options:

**Option A — Upload via browser (easiest for beginners):**
1. On your new repo page, click **"uploading an existing file"**
2. Drag and drop ALL files from the `qcommerce_dashboard` folder
3. Make sure to maintain the folder structure:
   ```
   qcommerce_dashboard/
   ├── app.py
   ├── data_loader.py
   ├── requirements.txt
   ├── README.md
   ├── data/
   │   └── me.xlsx
   ├── pages/
   │   ├── 1_Objective_3.py
   │   ├── 2_Objective_4.py
   │   ├── 3_Objective_5.py
   │   └── 4_About.py
   └── .streamlit/
       └── config.toml
   ```
4. Write commit message: `Initial dashboard upload`
5. Click **"Commit changes"**

**Option B — Git command line:**
```bash
cd qcommerce_dashboard
git init
git add .
git commit -m "Initial dashboard upload"
git remote add origin https://github.com/YOUR_USERNAME/qcommerce-vadodara-dashboard.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud (Free)

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in:
   - **Repository:** `YOUR_USERNAME/qcommerce-vadodara-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy!"**
6. Wait 2–3 minutes — your dashboard will be live at:
   `https://YOUR_USERNAME-qcommerce-vadodara-dashboard-app-XXXX.streamlit.app`

### Step 4: Share Your Dashboard

Copy the Streamlit URL and share it with your professor, committee, or anyone!

---

## 📁 Project Structure

```
qcommerce_dashboard/
├── app.py                    # Main entry point — Overview page
├── data_loader.py            # Shared data loading & all statistical computations
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   └── me.xlsx               # Survey data (341 respondents)
├── pages/
│   ├── 1_Objective_3.py      # Usage Behavior Analysis
│   ├── 2_Objective_4.py      # Key Drivers & EFA
│   ├── 3_Objective_5.py      # Predictive Models
│   └── 4_About.py            # About & Methods
└── .streamlit/
    └── config.toml           # Dark theme configuration
```

---

## ⚙️ Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/qcommerce-vadodara-dashboard.git
cd qcommerce-vadodara-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| Streamlit | Dashboard framework |
| Plotly | Interactive charts |
| SciPy | Statistical tests |
| scikit-learn | Logistic regression, cross-validation |
| NumPy / Pandas | Data processing |
| openpyxl | Excel file reading |

---

## 📬 Contact

**Department of Statistics**  
The Maharaja Sayajirao University of Baroda  
Vadodara, Gujarat, India
