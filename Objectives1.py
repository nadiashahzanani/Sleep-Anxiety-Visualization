import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Objective 1 — Distribution and Correlation")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Select fixed columns (based on your dataset order)
psqi_col = df.columns[8]   # Sleep Quality (PSQI)
anx_col = df.columns[6]    # Trait Anxiety

# --- Histogram 1: Sleep Quality ---
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots()
    sns.histplot(df[psqi_col], kde=True, color="skyblue", ax=ax)
    ax.set_title("Distribution of Sleep Quality (PSQI)")
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots()
    sns.histplot(df[anx_col], kde=True, color="salmon", ax=ax2)
    ax2.set_title("Distribution of Trait Anxiety")
    st.pyplot(fig2)

# --- Scatterplot: PSQI vs Anxiety ---
fig3, ax3 = plt.subplots()
sns.regplot(x=df[psqi_col], y=df[anx_col], scatter_kws={'alpha':0.6}, color="purple", ax=ax3)
r, p = stats.pearsonr(df[psqi_col].dropna(), df[anx_col].dropna())
ax3.text(0.02, 0.95, f"r = {r:.2f}, p = {p:.3g}", transform=ax3.transAxes)
ax3.set_xlabel("PSQI (Higher = Worse Sleep)")
ax3.set_ylabel("Trait Anxiety Score")
st.pyplot(fig3)

st.markdown(f"""
**Interpretation:**  
A moderate positive correlation (**r = {r:.2f}**) shows that poorer sleep quality tends to associate with higher anxiety.  
This supports Norbury & Evans (2018)’s findings that subjective sleep quality predicts anxiety among students.
""")
