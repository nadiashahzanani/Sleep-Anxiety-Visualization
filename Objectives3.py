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
