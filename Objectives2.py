import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Objective 2 — Group Comparisons and Chronotype")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Fixed columns
anx_col = df.columns[6]
sleep_cat_col = df.columns[9]
chrono_col = df.columns[5]
doze_col = df.columns[11]

# --- Boxplot: Trait Anxiety by Sleep Category ---
fig1, ax1 = plt.subplots()
sns.boxplot(x=sleep_cat_col, y=anx_col, data=df, palette="Set2", ax=ax1)
sns.stripplot(x=sleep_cat_col, y=anx_col, data=df, color="0.3", size=3, ax=ax1)
ax1.set_title("Trait Anxiety by Sleep Category")
st.pyplot(fig1)

# --- T-Test for anxiety levels ---
groups = [grp[anx_col].dropna() for _, grp in df.groupby(sleep_cat_col)]
if len(groups) == 2:
    t, p = stats.ttest_ind(groups[0], groups[1], equal_var=False)
    st.write(f"**T-test Result:** t = {t:.2f}, p = {p:.4f}")

st.markdown("""
**Interpretation:**  
Students with poor sleep tend to report higher anxiety levels.  
A significant t-test result supports the difference in anxiety between good and poor sleepers.
""")

# --- Bar Chart: Daytime Dozing by Sleep Category ---
st.subheader("Daytime Dozing by Sleep Category")
ctab = pd.crosstab(df[sleep_cat_col], df[doze_col], normalize='index') * 100
st.bar_chart(ctab)

st.markdown("""
**Interpretation:**  
Poor sleepers experience more frequent daytime dozing, suggesting sleep inefficiency affects daily alertness.
""")

# --- Violin Plot: Chronotype by Sleep Category ---
fig2, ax2 = plt.subplots()
sns.violinplot(x=sleep_cat_col, y=chrono_col, data=df, inner='quartile', palette="coolwarm", ax=ax2)
ax2.set_title("Chronotype (rMEQ) by Sleep Category")
st.pyplot(fig2)
