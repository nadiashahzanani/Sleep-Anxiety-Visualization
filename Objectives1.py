# ==============================================
# Sleep, Anxiety & Start Time Visualization App
# ==============================================

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

# ------------------------------------------------------------
# Variable Mapping (fixed, no sidebar)
# ------------------------------------------------------------
psqi_col = "PSQI_Score" if "PSQI_Score" in df.columns else df.columns[8]
anx_col = "Trait_Anxiety" if "Trait_Anxiety" in df.columns else df.columns[6]
chrono_col = "MEQ" if "MEQ" in df.columns else df.columns[5]
sleep_cat_col = "Sleep_Category" if "Sleep_Category" in df.columns else df.columns[9]
start_col = "Start_time_code" if "Start_time_code" in df.columns else df.columns[10]
doze_col = "Daytime_Dozing" if "Daytime_Dozing" in df.columns else df.columns[11]

# ============================================================
# Objective 1 — Distributions and Correlation
# ============================================================
st.header("Objective 1 — Distributions and Correlation")
st.markdown("""
This section describes the distribution of subjective sleep quality and trait anxiety among students 
and examines the relationship between both variables.
""")

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
    About **46% of students reported their sleep as 'fairly bad' or 'very bad'**,  
    which aligns with findings from Norbury & Evans (2018).
    """)

# --- Histogram: Trait Anxiety ---
with col2:
    fig2, ax2 = plt.subplots()
    sns.histplot(df[anx_col], kde=True, color="salmon", ax=ax2)
    ax2.set_title("Distribution of Trait Anxiety")
    st.pyplot(fig2)
    st.markdown("""
    **Interpretation:**  
    The trait anxiety scores show a broad distribution, ranging from low to high levels of anxiety, 
    suggesting variability in student mental wellbeing.
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
The scatterplot shows a **positive relationship** between PSQI and trait anxiety.  
Students with **poorer sleep quality** tend to report **higher anxiety levels**.  
The correlation (**r = {r:.2f}**, **p = {p:.3g}**) confirms a significant, moderate association.  
However, as this is a **cross-sectional dataset**, correlation does not imply causation.
""")

# --- Summary Box 1 ---
st.markdown("""
<div style="
    background-color:#f0f4ff;
    padding:15px;
    border-radius:10px;
    border-left:6px solid #4a90e2;
    margin-top:20px;">
<h4>📘 Summary Box</h4>
<p>
• Most students reported <b>fairly bad to very bad sleep quality</b>.<br>
• Trait anxiety scores increase with poorer sleep.<br>
• A <b>positive correlation</b> between PSQI and anxiety supports prior research.<br>
• Highlights the importance of sleep-focused wellbeing interventions.
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
st.markdown("---")
st.caption("Created by Nadia Shahzanani © 2025 | Scientific Visualization Project")
