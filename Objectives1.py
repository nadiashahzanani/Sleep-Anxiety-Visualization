# --- Import required libraries ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Page Title ---
st.title("Interactive Visualization — Objective 1 Analysis")

# --- Load dataset ---
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Dropdown to select Year of Study
year_filter = st.sidebar.multiselect(
    "Select Year(s) of Study:",
    options=sorted(df['Year_of_Study'].dropna().unique()),
    default=sorted(df['Year_of_Study'].dropna().unique())
)

# Dropdown to select Gender (Sex)
sex_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=sorted(df['Sex'].dropna().unique()),
    default=sorted(df['Sex'].dropna().unique())
)

# Filter the DataFrame based on selections
filtered_df = df[df['Year_of_Study'].isin(year_filter) & df['Sex'].isin(sex_filter)]

# --- Visualization 1: Gender Distribution by Year of Study ---
st.subheader("1. Gender Distribution by Year of Study")

fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.countplot(data=filtered_df, x='Year_of_Study', hue='Sex', palette='Set2', ax=ax1)
ax1.set_title("Gender Distribution by Year of Study", fontsize=12)
ax1.set_xlabel("Year of Study")
ax1.set_ylabel("Number of Students")
ax1.legend(title='Sex', loc='upper right')
st.pyplot(fig1)

# --- Dynamic Text Summary ---
st.markdown(f"""
**Interactive Interpretation:**

- You are currently viewing **{len(filtered_df)} students** filtered by:
  - Year(s) of Study: `{', '.join(map(str, year_filter))}`
  - Gender(s): `{', '.join(map(str, sex_filter))}`

**Interpretation:**
1. The chart shows how student counts vary by year and gender based on your filter.
2. You can adjust the filters in the sidebar to focus on specific groups (e.g., only Year 1, or only male students).
3. This helps explore whether certain study years have more balanced or skewed gender distributions.
""")


# --- Visualization 2: Distribution of Sleep Quality (PSQI) ---
st.subheader("2. Distribution of Sleep Quality (PSQI)")

fig2, ax2 = plt.subplots(figsize=(7, 4))
sns.histplot(df['psqi_2_groups'], kde=True, color='skyblue', bins=5, ax=ax2)
ax2.set_title("Distribution of Sleep Quality (PSQI)", fontsize=12)
ax2.set_xlabel("PSQI Score (Higher = Poorer Sleep)")
ax2.set_ylabel("Number of Students")
st.pyplot(fig2)

st.markdown("""
**Interpretation:**
1. Most students fall into two groups — one with good sleep (low PSQI = 1) and another with poor sleep (high PSQI = 2).  
2. Few students fall in between, showing sleep is either good or poor, not moderate.  
3. The distribution is **bimodal**, with peaks at PSQI = 1 and 2.  
4. This suggests two clear sleep patterns — good vs. poor sleepers.
""")


# --- Visualization 3: Sleep Quality (PSQI) by Year of Study ---
st.subheader("3. Sleep Quality (PSQI) by Year of Study")

fig3, ax3 = plt.subplots(figsize=(7, 4))
sns.boxplot(data=df, x='Year_of_Study', y='psqi_2_groups', palette='pastel', ax=ax3)
ax3.set_title("Sleep Quality (PSQI) by Year of Study", fontsize=12)
ax3.set_xlabel("Year of Study")
ax3.set_ylabel("PSQI Score (1 = Good, 2 = Poor)")
st.pyplot(fig3)

st.markdown("""
**Interpretation:**
1. Students from Year 1 and 2 show similar PSQI scores, indicating a mix of good and poor sleepers.  
2. Year 3 students mostly report good sleep quality (score = 1).  
3. Overall, sleep quality doesn’t change drastically across years, but third-year students may sleep slightly better on average.
""")
