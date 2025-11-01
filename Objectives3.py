import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Objective 3 — Preferred Start Time & Correlation Matrix")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Fixed columns
psqi_col = df.columns[8]
anx_col = df.columns[6]
chrono_col = df.columns[5]
start_col = df.columns[10]

# --- Preferred Start Time by Chronotype ---
st.subheader("Preferred Start Time by Chronotype")
ctab = pd.crosstab(df[start_col], df[chrono_col])
st.bar_chart(ctab)

st.markdown("""
**Interpretation:**  
Students with morning chronotypes prefer earlier start times,  
while evening chronotypes prefer later classes.
""")

# --- Scatterplot: Anxiety vs Sleep Quality by Start Time ---
st.subheader("Scatterplot: Anxiety vs PSQI by Start Time")
fig, ax = plt.subplots()
sns.scatterplot(x=psqi_col, y=anx_col, hue=start_col, data=df, ax=ax)
st.pyplot(fig)

st.markdown("""
**Interpretation:**  
Later start preferences are linked to both poorer sleep quality and higher anxiety levels.
""")

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap")
numeric = df.select_dtypes(include='number')
corr = numeric.corr()
fig2, ax2 = plt.subplots(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap="vlag", ax=ax2)
st.pyplot(fig2)
