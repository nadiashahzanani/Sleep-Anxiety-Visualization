import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Objective 1 — Distribution and Correlation")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Histogram: Sleep Quality (PSQI) and Trait Anxiety ---
col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(df['psqi_2_groups'], kde=True, color='skyblue', ax=ax)
    ax.set_title("Distribution of Sleep Quality (PSQI)", fontsize=12)
    ax.set_xlabel("PSQI Score (Higher = Poorer Sleep)")
    ax.set_ylabel("Number of Students")
    st.pyplot(fig)

with col2:
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    sns.histplot(df['Trait_Anxiety'], kde=True, color='salmon', ax=ax2)
    ax2.set_title("Distribution of Trait Anxiety", fontsize=12)
    ax2.set_xlabel("Trait Anxiety Score")
    ax2.set_ylabel("Number of Students")
    st.pyplot(fig2)

# --- Scatterplot with Regression: PSQI vs Trait Anxiety ---
fig3, ax3 = plt.subplots(figsize=(7, 5))
sns.regplot(x='psqi_2_groups', y='Trait_Anxiety', data=df, scatter_kws={'alpha':0.6}, color='purple', ax=ax3)
r, p = stats.pearsonr(df['psqi_2_groups'].dropna(), df['Trait_Anxiety'].dropna())
ax3.text(0.02, 0.95, f"r = {r:.2f}, p = {p:.4f}", transform=ax3.transAxes)
ax3.set_xlabel("PSQI (Higher = Worse Sleep)")
ax3.set_ylabel("Trait Anxiety Score")
ax3.set_title("Relationship Between Sleep Quality and Trait Anxiety")
st.pyplot(fig3)

st.markdown(f"""
**Interpretation:**  
A positive correlation (**r = {r:.2f}**) indicates that students with poorer sleep (higher PSQI scores)  
tend to have higher anxiety levels. This pattern mirrors findings by Norbury & Evans (2018).
""")
