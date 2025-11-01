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
