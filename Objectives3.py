import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Objective 3 — Preferred Start Time & Correlation Matrix")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Bar Chart: Preferred University Start Time by Sleep Category ---
st.subheader("Preferred University Start Time by Sleep Category")

if 'Start_time_code' in df.columns and 'sleep_category' in df.columns:
    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(7,4))
    sns.countplot(x='Start_time_code', hue='sleep_category', data=df, palette='muted', ax=ax)
    ax.set_title("Preferred University Start Time by Sleep Category")
    ax.set_xlabel("Preferred Start Time Code")
    ax.set_ylabel("Number of Students")
    ax.legend(title="Sleep Category")
    st.pyplot(fig)
else:
    st.warning("⚠️ Column 'Start_time_code' or 'sleep_category' not found in dataset.")


st.markdown("""
**Interpretation:**  
Students with **poorer sleep quality** tend to prefer **later university start times**,  
while good sleepers are more likely to choose earlier classes.  
This pattern aligns with known chronotype behavior — *evening-type individuals* often experience 
delayed sleep cycles and prefer later activity schedules.
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
