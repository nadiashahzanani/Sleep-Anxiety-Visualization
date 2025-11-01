# ============================================================
# Objective 2 — Group Comparisons and Chronotype (Upgraded)
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# ------------------------------------------------------------
# Page Setup
# ------------------------------------------------------------
st.title("Objective 2 — Group Comparisons and Chronotype")
st.markdown("""
This page compares **Trait Anxiety** across **Sleep Categories** and explores how **Chronotype (rMEQ)** 
and **Daytime Dozing** vary between good and poor sleepers, 
as described in *Norbury & Evans (2018)*.
""")

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# ------------------------------------------------------------
# Boxplot: Trait Anxiety by Sleep Category
# ------------------------------------------------------------
st.subheader("1️⃣ Trait Anxiety by Sleep Quality Category")

fig1, ax1 = plt.subplots(figsize=(6, 4))
sns.boxplot(x='sleep_category', y='Trait_Anxiety', data=df, palette='Set2', ax=ax1)
sns.swarmplot(x='sleep_category', y='Trait_Anxiety', data=df, color='0.3', size=3, ax=ax1)
ax1.set_title("Trait Anxiety by Sleep Quality Category")
ax1.set_xlabel("Sleep Category")
ax1.set_ylabel("Trait Anxiety Score")
st.pyplot(fig1)

# --- Statistical Test (T-Test)
good = df[df['sleep_category'] == 'Good Sleep']['Trait_Anxiety']
poor = df[df['sleep_category'] == 'Poor Sleep']['Trait_Anxiety']
t, p = stats.ttest_ind(good, poor)

st.markdown(f"**T-test Result:** t = `{t:.3f}`, p = `{p:.4f}`")

st.markdown("""
**Interpretation:**  
Students with **Poor Sleep** tend to have **higher trait anxiety** on average.  
The t-test result confirms a significant difference between the two groups 
(see *t* and *p* values above).
""")

# ------------------------------------------------------------
# Bar Chart: Daytime Dozing by Sleep Category
# ------------------------------------------------------------
st.subheader("2️⃣ Daytime Dozing Frequency by Sleep Quality Category")

if 'Daytime_Dozing' in df.columns:
    doze_counts = pd.crosstab(df['sleep_category'], df['Daytime_Dozing'], normalize='index') * 100
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    doze_counts.plot(kind='bar', stacked=True, colormap='coolwarm', ax=ax2)
    ax2.set_title("Daytime Dozing Frequency by Sleep Quality Category")
    ax2.set_xlabel("Sleep Category")
    ax2.set_ylabel("Percentage")
    ax2.legend(title="Dozing Frequency")
    st.pyplot(fig2)
else:
    st.warning("⚠️ Column 'Daytime_Dozing' not found in dataset.")

st.markdown("""
**Interpretation:**  
Daytime dozing is **more frequent among poor sleepers**, indicating possible effects of reduced nighttime rest 
on daytime alertness and cognitive performance.
""")

# ------------------------------------------------------------
# Violin Plot: Chronotype (rMEQ) by Sleep Category
# ------------------------------------------------------------
st.subheader("3️⃣ Chronotype (rMEQ) by Sleep Quality Category")

fig3, ax3 = plt.subplots(figsize=(7, 4))
sns.violinplot(x='sleep_category', y='MEQ', data=df, palette='coolwarm', inner='quartile', ax=ax3)
ax3.set_title("Chronotype (rMEQ Score) by Sleep Quality Category")
ax3.set_xlabel("Sleep Category")
ax3.set_ylabel("rMEQ Score (Higher = Morning Type)")
st.pyplot(fig3)

st.markdown("""
**Interpretation:**  
Students with **Poor Sleep Quality** generally show **lower rMEQ scores**, indicating a shift toward **evening chronotype**.  
This pattern suggests that individuals who are more “evening-type” might experience poorer sleep and higher anxiety.
""")

# ------------------------------------------------------------
# Summary Box
# ------------------------------------------------------------
st.markdown("""
<div style="
    background-color:#f9f9f9;
    padding:15px;
    border-radius:10px;
    border-left:6px solid #90c978;
    margin-top:20px;">
<h4>📘 Summary Box</h4>
<p>
• <b>Higher anxiety</b> among poor sleepers confirmed via t-test.<br>
• <b>Daytime dozing</b> is more common in poor sleepers.<br>
• <b>Evening chronotypes</b> tend to have worse sleep and higher anxiety.<br>
• Findings are consistent with Norbury & Evans (2018) and support 
  links between <b>sleep quality, circadian rhythm, and mental health.</b>
</p>
</div>
""", unsafe_allow_html=True)
