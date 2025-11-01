import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

# Load data
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

st.header("Objective 1 — Distribution and Correlation")
st.markdown("This page explores how students’ **sleep quality** relates to **trait anxiety**.")

# 1️⃣ Sleep Quality Distribution
fig1 = px.histogram(df, x="psqi_2_groups", color_discrete_sequence=["#4a90e2"], title="Distribution of Sleep Quality")
st.plotly_chart(fig1, use_container_width=True)
st.write("**Interpretation:** Most students report moderate to poor sleep quality, consistent with university samples.")

# 2️⃣ Trait Anxiety Distribution
fig2 = px.histogram(df, x="Trait_Anxiety", color_discrete_sequence=["#f45b69"], title="Distribution of Trait Anxiety Scores")
st.plotly_chart(fig2, use_container_width=True)
st.write("**Interpretation:** Anxiety levels vary widely, reflecting diverse psychological wellbeing across students.")

# 3️⃣ Correlation (Sleep vs Anxiety)
r, p = stats.pearsonr(df["psqi_2_groups"].dropna(), df["Trait_Anxiety"].dropna())
fig3 = px.scatter(df, x="psqi_2_groups", y="Trait_Anxiety", trendline="ols",
                  color_discrete_sequence=["#90c978"],
                  title=f"Relationship Between Sleep Quality and Anxiety (r = {r:.2f}, p = {p:.3g})")
st.plotly_chart(fig3, use_container_width=True)
st.write("**Interpretation:** Poorer sleep quality (higher PSQI) is associated with higher anxiety levels (moderate positive correlation).")
