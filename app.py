# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import statsmodels.api as sm

st.set_page_config(layout="wide", page_title="Sleep, Anxiety & Start Time — Visualisation Report")

@st.cache_data
def load_data(path="/content/Time_to_think_Norburyy.csv"):
    df = pd.read_csv(path)
    return df

st.title("Time to think: Subjective sleep quality, trait anxiety and university start time")
st.markdown("Data source: Norbury & Evans (Mendeley Data) — DOI: 10.17632/mxsjysrt8j.1. Cite: Norbury R., Evans S. 2018. :contentReference[oaicite:9]{index=9}")

# Load
try:
    df = load_data()
except Exception as e:
    st.error("Could not find 'norbury_sleep_data.csv' in this folder. Please download from Mendeley Data and rename it: norbury_sleep_data.csv")
    st.stop()

# Quick cleaning: adapt column names to actual dataset
st.sidebar.header("Controls")
# NOTE: below column names are guesses — adjust according to actual CSV headers
st.sidebar.markdown("Adjust column names in app.py if needed.")

# Explore columns
st.sidebar.subheader("Dataset columns")
st.sidebar.write(list(df.columns))

# Page selector
page = st.sidebar.radio("Choose page", ["Page 1 — Distributions", "Page 2 — Group comparisons", "Page 3 — Start time & correlations"])

#####################
# PAGE 1
#####################
if page == "Page 1 — Distributions":
    st.header("Objective 1 — Distributions & basic relationship")
    st.write("Objective: Describe distributions of sleep quality and trait anxiety; examine correlation.")
    col1, col2 = st.columns(2)

    # Column names (edit these to exact column names)
    psqi_col = st.selectbox("Select PSQI / sleep quality column", options=df.columns, index=0)
    anxiety_col = st.selectbox("Select trait anxiety column", options=df.columns, index=1)
    gender_col = st.selectbox("Select gender column (optional)", options=[None]+list(df.columns), index=0)

    # Histograms
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(df[psqi_col].dropna(), kde=True, ax=ax)
    ax.set_title("Distribution of PSQI / subjective sleep quality")
    st.pyplot(fig)

    fig2, ax2 = plt.subplots(figsize=(6,4))
    sns.histplot(df[anxiety_col].dropna(), kde=True, ax=ax2)
    ax2.set_title("Distribution of trait anxiety")
    st.pyplot(fig2)

    # Scatter + regression
    fig3, ax3 = plt.subplots(figsize=(7,5))
    sns.regplot(x=df[psqi_col], y=df[anxiety_col], scatter_kws={'s':20}, ax=ax3)
    ax3.set_xlabel("PSQI (higher = worse)")
    ax3.set_ylabel("Trait anxiety")
    r, p = stats.pearsonr(df[psqi_col].dropna(), df[anxiety_col].dropna())
    ax3.text(0.02, 0.95, f"Pearson r = {r:.3f}, p = {p:.3g}", transform=ax3.transAxes)
    st.pyplot(fig3)

    st.write("Interpretation: The plot above shows the association between sleep quality and trait anxiety. Report Pearson r above.")

#####################
# PAGE 2
#####################
if page == "Page 2 — Group comparisons":
    st.header("Objective 2 — Group comparisons by sleep quality & chronotype")
    st.write("Objective: Compare trait anxiety and daytime dozing by sleep quality; examine chronotype differences.")

    # Select columns
    sleep_cat_col = st.selectbox("Select sleep category column (binary/categorical good vs poor)", options=df.columns, index=2)
    daytime_col = st.selectbox("Select daytime dozing column (binary)", options=df.columns, index=3)
    rmeq_col = st.selectbox("Select rMEQ/chronotype column", options=df.columns, index=4)

    # Boxplot trait anxiety by sleep category
    fig4, ax4 = plt.subplots(figsize=(7,4))
    sns.boxplot(x=df[sleep_cat_col], y=df[anxiety_col], ax=ax4)
    sns.swarmplot(x=df[sleep_cat_col], y=df[anxiety_col], color='0.3', size=3, ax=ax4)
    ax4.set_title("Trait anxiety by sleep quality category")
    st.pyplot(fig4)

    # statistical test
    groups = [grp[anxiety_col].dropna().values for name, grp in df.groupby(sleep_cat_col)]
    if len(groups) >= 2:
        try:
            tstat, pval = stats.ttest_ind(*groups, nan_policy='omit')
            st.write(f"T-test between categories: t = {tstat:.3f}, p = {pval:.3g}")
        except Exception:
            st.write("Could not perform t-test (check group sizes/assumptions).")

    # Bar chart: daytime dozing by sleep category
    ctab = pd.crosstab(df[sleep_cat_col], df[daytime_col], normalize='index')*100
    st.write("Daytime dozing proportions by sleep category")
    st.bar_chart(ctab)

    # Violin for rMEQ by sleep category
    fig5, ax5 = plt.subplots(figsize=(7,4))
    sns.violinplot(x=df[sleep_cat_col], y=df[rmeq_col], inner='quartile', ax=ax5)
    sns.stripplot(x=df[sleep_cat_col], y=df[rmeq_col], color='0.2', size=3, jitter=True, ax=ax5)
    ax5.set_title("rMEQ (chronotype) by sleep category")
    st.pyplot(fig5)

#####################
# PAGE 3
#####################
if page == "Page 3 — Start time & correlations":
    st.header("Objective 3 — Start times, chronotype and correlation structure")
    st.write("Objective: Visualize preferred start times and the multivariate correlation structure.")

    start_col = st.selectbox("Select preferred start time column", options=df.columns, index=5)
    # Preferred start time distribution
    st.write("Preferred start time distribution (counts):")
    st.bar_chart(df[start_col].value_counts())

    # Faceted scatter (anxiety vs PSQI) by start time
    st.write("Scatter — trait anxiety vs PSQI faceted by preferred start time")
    # For simplicity show scatter colored by start category
    fig6, ax6 = plt.subplots(figsize=(8,6))
    sns.scatterplot(x=df[psqi_col], y=df[anxiety_col], hue=df[start_col], ax=ax6)
    ax6.set_xlabel("PSQI")
    ax6.set_ylabel("Trait anxiety")
    st.pyplot(fig6)

    # Correlation heatmap
    st.write("Correlation heatmap (numeric columns):")
    numeric = df.select_dtypes(include=[np.number])
    corr = numeric.corr()
    fig7, ax7 = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", ax=ax7)
    st.pyplot(fig7)

    st.write("Interpretation: Use the heatmap to identify strong correlations (e.g., PSQI vs trait anxiety).")

st.sidebar.markdown("---")
st.sidebar.write("Dataset citation: Norbury R., Evans S. (2018). Time to think: Subjective sleep quality, trait anxiety and university start time. Mendeley Data. DOI: 10.17632/mxsjysrt8j.1")
