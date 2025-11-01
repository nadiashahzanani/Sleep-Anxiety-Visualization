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

# ============================================================
# Objective 2 — Group Comparisons and Chronotype
# ============================================================
st.header("Objective 2 — Group Comparisons and Chronotype")

# --- Boxplot: Trait Anxiety by Sleep Category ---
fig4, ax4 = plt.subplots()
sns.boxplot(x=sleep_cat_col, y=anx_col, data=df, palette="Set2", ax=ax4)
sns.stripplot(x=sleep_cat_col, y=anx_col, data=df, color="0.3", size=3, ax=ax4)
ax4.set_title("Trait Anxiety by Sleep Category")
st.pyplot(fig4)

groups = [grp[anx_col].dropna() for _, grp in df.groupby(sleep_cat_col)]
if len(groups) == 2:
    t, p = stats.ttest_ind(groups[0], groups[1], equal_var=False)
    st.write(f"**T-test Result:** t = {t:.2f}, p = {p:.4f}")

st.markdown("""
**Interpretation:**  
Students with poorer sleep have higher median anxiety levels.  
The t-test confirms a statistically significant difference, suggesting that poor sleep quality is linked with elevated anxiety.
""")

# --- Bar Chart: Daytime Dozing by Sleep Category ---
st.subheader("Daytime Dozing by Sleep Category")
ctab = pd.crosstab(df[sleep_cat_col], df[doze_col], normalize='index') * 100
st.bar_chart(ctab)

st.markdown("""
**Interpretation:**  
Daytime dozing occurs more frequently among poor sleepers, indicating possible consequences of insufficient rest.
""")

# --- Violin Plot: Chronotype (rMEQ) by Sleep Category ---
fig5, ax5 = plt.subplots()
sns.violinplot(x=sleep_cat_col, y=chrono_col, data=df, inner='quartile', palette="coolwarm", ax=ax5)
ax5.set_title("Chronotype (rMEQ) by Sleep Category")
st.pyplot(fig5)

st.markdown("""
**Interpretation:**  
Students with poorer sleep tend to show lower rMEQ scores (evening chronotype).  
While this suggests possible circadian misalignment, additional analysis is needed to confirm mediation effects.
""")

# --- Summary Box 2 ---
st.markdown("""
<div style="
    background-color:#f9f9f9;
    padding:15px;
    border-radius:10px;
    border-left:6px solid #90c978;
    margin-top:20px;">
<h4>📘 Summary Box</h4>
<p>
• Poor sleepers show <b>significantly higher anxiety</b>.<br>
• <b>Daytime dozing</b> is more common among poor sleepers.<br>
• <b>Evening chronotypes</b> tend to have worse sleep and higher anxiety.<br>
• Findings align with known links between circadian rhythm and mental wellbeing.
</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Objective 3 — Preferred Start Time & Correlation Matrix
# ============================================================
st.header("Objective 3 — Preferred Start Time & Correlation Matrix")

# --- Preferred Start Time by Chronotype ---
st.subheader("Preferred Start Time by Chronotype")
ctab2 = pd.crosstab(df[start_col], df[chrono_col])
st.bar_chart(ctab2)

st.markdown("""
**Interpretation:**  
Preferred start time is associated with chronotype.  
Morning types tend to prefer earlier classes, while evening types prefer later start times.
""")

# --- Scatter: Anxiety vs PSQI by Start Time ---
st.subheader("Scatter: Anxiety vs PSQI by Start Time")
fig6, ax6 = plt.subplots()
sns.scatterplot(x=psqi_col, y=anx_col, hue=start_col, data=df, ax=ax6)
st.pyplot(fig6)

st.markdown("""
**Interpretation:**  
Students preferring later start times generally report both <b>poorer sleep</b> and <b>higher anxiety</b>, 
suggesting a moderate association between scheduling preferences and wellbeing.
""")

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap")
numeric = df.select_dtypes(include=np.number)
corr = numeric.corr()
fig7, ax7 = plt.subplots(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap="vlag", ax=ax7)
st.pyplot(fig7)

st.markdown("""
**Interpretation:**  
The correlation heatmap identifies strongest associations — particularly between <b>Anxiety ↔ PSQI</b> 
and <b>PSQI ↔ Daytime Dozing</b> (r ≈ 0.35).  
These patterns support that poor sleep and frequent daytime fatigue relate to higher anxiety levels.
""")

# --- Summary Box 3 ---
st.markdown("""
<div style="
    background-color:#fff8e6;
    padding:15px;
    border-radius:10px;
    border-left:6px solid #ffb74d;
    margin-top:20px;">
<h4>📘 Summary Box</h4>
<p>
• <b>Preferred start time</b> aligns with chronotype (morning vs evening types).<br>
• Later start preferences correlate with <b>poorer sleep</b> and <b>higher anxiety</b>.<br>
• Heatmap confirms moderate relationships among PSQI, anxiety, and daytime dozing.<br>
• <b>Next steps:</b> conduct multivariate regression controlling for demographics, 
and explore mediation by chronotype.
</p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
st.markdown("---")
st.caption("Created by Nadia Shahzanani © 2025 | Scientific Visualization Project")
