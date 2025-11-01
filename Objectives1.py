import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Objective 1 — Distribution and Correlation")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Histogram of Sleep Quality (PSQI) ---

plt.figure(figsize=(7,4))
sns.histplot(df['psqi_2_groups'], kde=True, color='skyblue')
plt.title("Distribution of Sleep Quality (PSQI)")
plt.xlabel("PSQI Score (Higher = Poorer Sleep)")
plt.ylabel("Number of Students")
plt.show()

# --- Interpretation ---
interpretation = """
Interpretation:
1. Most students fall into two groups — one with good sleep (low PSQI score = 1) and another with poor sleep (high PSQI score = 2). 
2. Very few students are in between, meaning their sleep quality is either good or bad, not moderate.
3. The distribution is bimodal, with peaks at PSQI = 1 and PSQI = 2, and almost no middle values.
4. This indicates that students tend to cluster into two clear categories — good vs. poor sleepers — suggesting distinct sleep patterns rather than a continuous range.
"""

print(interpretation)

