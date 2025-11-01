# ============================================================
# Sleep, Anxiety & Start Time Visualization App
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(page_title="Sleep, Anxiety & Start Time Visualization", layout="wide")
st.title("🧠 Time to Think — Sleep, Anxiety and University Start Time")
st.markdown("""
Dataset: **Norbury & Evans (2018)**, Mendeley Data V1  
DOI: [10.17632/mxsjysrt8j.1](https://doi.org/10.17632/mxsjysrt8j.1)
""")
st.markdown("---")

# ------------------------------------------------------------
# Load Dataset (from GitHub)
# ------------------------------------------------------------
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

try:
    df = load_data(url)
    st.success("✅ Dataset successfully loaded from GitHub.")
except Exception as e:
    st.error("❌ Error loading dataset. Please check your file URL or name.")
    st.stop()

st.write("### Dataset Preview")
st.dataframe(df.head())

# Sidebar Navigation
page = st.sidebar.radio("Select Page", ["Page 1", "Page 2", "Page 3"])

# Sidebar Variable Mapping
st.sidebar.header("Variable Mapping")
psqi_col = st.sidebar.selectbox("Sleep Quality (PSQI)", df.columns, index=8)
anx_col  = st.sidebar.selectbox("Trait Anxiety", df.columns, index=6)
chrono_col = st.sidebar.selectbox("Chronotype (rMEQ)", df.columns, index=5)
sleep_cat_col = st.sidebar.selectbox("Sleep Category", df.columns, index=9)
start_col = st.sidebar.selectbox("Preferred Start Time", df.columns, index=10)
doze_col = st.sidebar.selectbox("Daytime Dozing", df.columns, index=11)

# ============================================================
# PAGE 1: Distributions and Correlation
# ============================================================
if page == "Page 1":
    st.header("Objective 1 — Distributions and Correlation")
    st.markdown("This section describes the distribution of subjective sleep quality and trait anxiety in the student sample and examines the relationship between both variables.")

    col1, col2 = st.columns(2)

    # --- Histogram: PSQI Sleep Quality ---
    with col1:
        fig, ax = plt.subplots()
        sns.histplot(df[psqi_col], kde=True, color="skyblue", ax=ax)
        ax.set_title("Distribution of Sleep Quality (PSQI)")
        st.pyplot(fig)
        st.markdown("""
        **Interpretation:**  
        The PSQI-based sleep quality shows a multimodal or ordinal distribution.  
        About **46% of students reported their sleep as 'fairly bad' or 'very bad'**, which is clearly reflected in the histogram.  
        This pattern aligns with the findings from the Brunel University Research Archive (Norbury & Evans, 2018).
        """)

    # --- Histogram: Trait Anxiety ---
    with col2:
        fig2, ax2 = plt.subplots()
        sns.histplot(df[anx_col], kde=True, color="salmon", ax=ax2)
        ax2.set_title("Distribution of Trait Anxiety")
        st.pyplot(fig2)
        st.markdown("""
        **Interpretation:**  
        The trait anxiety scores display a continuous, near-normal distribution.  
        This suggests a broad range of anxiety levels among students, from low to high,  
        which helps reveal how anxiety may vary according to sleep quality differences.
        """)

    # --- Scatterplot with Regression: PSQI vs Trait Anxiety ---
    fig3, ax3 = plt.subplots()
    sns.regplot(x=df[psqi_col], y=df[anx_col], scatter_kws={'alpha':0.6}, color="purple", ax=ax3)
    r, p = stats.pearsonr(df[psqi_col].dropna(), df[anx_col].dropna())
    ax3.text(0.02, 0.95, f"r = {r:.2f}, p = {p:.3g}", transform=ax3.transAxes)
    ax3.set_xlabel("PSQI (Higher = Worse Sleep)")
    ax3.set_ylabel("Trait Anxiety Score")
    st.pyplot(fig3)

    st.markdown(f"""
    **Interpretation:**  
    The scatterplot and regression line demonstrate a **positive relationship** between PSQI and trait anxiety.  
    Students with **higher PSQI scores (indicating poorer sleep quality)** tend to report **higher anxiety levels**.  
    The computed Pearson correlation (**r = {r:.2f}**, **p = {p:.3g}**) quantifies the strength and significance of this relationship.  

    While this association is consistent with existing research, it’s important to note that this is a **cross-sectional design**,  
    meaning the results indicate correlation, not causation. Additionally, responses are **self-reported**,  
    which introduces the potential for response bias.
    """)

    st.markdown("---")
    st.caption("Page 1 visualizations summarize the key distribution patterns and correlations between sleep quality and anxiety.")


# ============================================================
# PAGE 2: Group Comparisons and Chronotype
# ============================================================
if page == "Page 2":
    st.header("Objective 2 — Group Comparisons and Chronotype")

    # --- Boxplot: Trait Anxiety by Sleep Category ---
    fig4, ax4 = plt.subplots()
    sns.boxplot(x=sleep_cat_col, y=anx_col, data=df, palette="Set2", ax=ax4)
    sns.stripplot(x=sleep_cat_col, y=anx_col, data=df, color="0.3", size=3, ax=ax4)
    ax4.set_title("Trait Anxiety by Sleep Category")
    st.pyplot(fig4)

    # T-test to compare anxiety between good vs poor sleepers
    groups = [grp[anx_col].dropna() for _, grp in df.groupby(sleep_cat_col)]
    if len(groups) == 2:
        t, p = stats.ttest_ind(groups[0], groups[1], equal_var=False)
        st.write(f"**T-test Result:** t = {t:.2f}, p = {p:.4f}")

    # --- Interpretation for Boxplot ---
    st.markdown("""
    **Interpretation:**  
    The boxplot shows that students with poorer sleep tend to have higher median anxiety levels.  
    This is supported by the T-test result, which indicates a statistically significant difference in anxiety between good and poor sleepers (report *t* and *p* above).  
    This suggests that poorer subjective sleep quality is associated with higher levels of anxiety among university students.
    """)

    # --- Bar Chart: Daytime Dozing by Sleep Category ---
    st.markdown("#### Daytime Dozing by Sleep Category")
    ctab = pd.crosstab(df[sleep_cat_col], df[doze_col], normalize='index') * 100
    st.bar_chart(ctab)

    # --- Interpretation for Daytime Dozing ---
    st.markdown("""
    **Interpretation:**  
    The bar chart reveals that daytime dozing is more common among poor sleepers.  
    This supports the idea that insufficient or low-quality nighttime sleep may lead to increased daytime fatigue or sleepiness,  
    a plausible functional consequence observed in students with poorer sleep quality.
    """)

    # --- Violin Plot: Chronotype (rMEQ) by Sleep Category ---
    fig5, ax5 = plt.subplots()
    sns.violinplot(x=sleep_cat_col, y=chrono_col, data=df, inner='quartile', palette="coolwarm", ax=ax5)
    ax5.set_title("Chronotype (rMEQ) by Sleep Category")
    st.pyplot(fig5)

    # --- Interpretation for Chronotype ---
    st.markdown("""
    **Interpretation:**  
    The violin plot suggests that students with poorer sleep quality tend to show lower rMEQ scores,  
    indicating a shift toward eveningness chronotype patterns.  
    While this might imply a relationship between being an “evening type” and poor sleep or higher anxiety,  
    formal mediation analysis (such as regression or bootstrapping) is needed to test this statistically.  
    The original study reported that chronotype did **not** mediate the sleep–anxiety relationship,  
    so this visualization provides descriptive support for that conclusion rather than causal evidence.
    """)


# ============================================================
# PAGE 3: Preferred Start Time & Correlation Matrix
# ============================================================
if page == "Page 3":
    st.header("Objective 3 — Preferred Start Time & Correlation Matrix")

    st.subheader("Preferred Start Time by Chronotype")
    ctab2 = pd.crosstab(df[start_col], df[chrono_col])
    st.bar_chart(ctab2)

    st.subheader("Scatter: Anxiety vs PSQI by Start Time")
    fig6, ax6 = plt.subplots()
    sns.scatterplot(x=psqi_col, y=anx_col, hue=start_col, data=df, ax=ax6)
    st.pyplot(fig6)

    st.subheader("Correlation Heatmap")
    numeric = df.select_dtypes(include=np.number)
    corr = numeric.corr()
    fig7, ax7 = plt.subplots(figsize=(7,5))
    sns.heatmap(corr, annot=True, cmap="vlag", ax=ax7)
    st.pyplot(fig7)

    st.markdown("""
    **Interpretation:**  
    The correlation matrix shows strong associations between sleep quality, anxiety, and chronotype measures.
    Students preferring later start times also exhibit poorer sleep quality and higher anxiety levels.
    """)

st.markdown("---")
st.caption("Created by Nadia Shahzanani © 2025 | Scientific Visualization Project")
