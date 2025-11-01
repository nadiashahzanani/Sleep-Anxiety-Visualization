import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Objective 3 — Preferred Start Time & Correlation Matrix")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Fixed column names (adjust as per your dataset)
psqi_col = "PSQI_Score" if "PSQI_Score" in df.columns else df.columns[8]
anx_col = "Trait_Anxiety" if "Trait_Anxiety" in df.columns else df.columns[6]
chrono_col = "MEQ" if "MEQ" in df.columns else df.columns[5]
sleep_cat_col = "sleep_category" if "sleep_category" in df.columns else df.columns[9]
start_col = "Start_time_code" if "Start_time_code" in df.columns else df.columns[10]

# --- Bar Chart: Preferred Start Time by Sleep Category ---
st.subheader("Preferred University Start Time by Sleep Category")

# ✅ Match Google Colab’s output (remove warning)
fig, ax = plt.subplots(figsize=(7,4))
sns.countplot(x=start_col, hue=sleep_cat_col, data=df, palette='muted', ax=ax)
ax.set_title("Preferred University Start Time by Sleep Category")
ax.set_xlabel("Preferred Start Time Code")
ax.set_ylabel("Number of Students")
ax.legend(title="Sleep Category")
st.pyplot(fig)

st.markdown("""
**Interpretation:**  
This chart shows how students’ preferred class start times relate to their sleep category.  
Students with **poorer sleep quality** often prefer **later start times**, while good sleepers prefer earlier classes.  
This pattern supports the idea that evening chronotypes align with delayed daily schedules.
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
