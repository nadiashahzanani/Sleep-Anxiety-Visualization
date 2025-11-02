# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page title ---
st.subheader("1. Gender Representation by Year Level")

# --- Load dataset ---
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- 1. Gender Distribution by Year of Study ---
fig_gender = px.bar(
    df,
    x='Year_of_Study',
    color='Sex',
    barmode='group',
    title='Gender Distribution by Year of Study',
    labels={'Year_of_Study': 'Year of Study', 'Sex': 'Gender'}
)

fig_gender.update_layout(
    yaxis_title="Number of Students",
    xaxis_title="Year of Study",
    title_x=0.3,
    legend_title="Click to Hide/Show Gender",
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode="x unified"
)

st.plotly_chart(fig_gender, use_container_width=True)

st.markdown("**Interpretation:**")
st.markdown("""
- This chart shows the gender distribution across different years of study.
- Both male and female students are present in every year, with slightly more students in the earlier years.
""")

# --- 2. Sleep Quality Distribution (Histogram) ---
st.subheader("2. Basic Sleep Quality Distribution")

fig_sleep = px.histogram(
    df,
    x='psqi_2_groups',
    color='psqi_2_groups',
    nbins=10,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Distribution of Sleep Quality (PSQI)"
)

fig_sleep.update_layout(
    xaxis_title="PSQI Score (Higher = Poorer Sleep)",
    yaxis_title="Number of Students",
    bargap=0.1,
    template="simple_white",
    legend_title_text="PSQI Group"
)
fig_sleep.update_traces(opacity=0.8)

st.plotly_chart(fig_sleep, use_container_width=True)

st.markdown("**Interpretation:**")
st.markdown("""
- Most students fall into two main sleep quality categories: good sleepers (PSQI = 1) and poor sleepers (PSQI = 2).  
- The interactive legend allows exploring each group's contribution to the overall pattern.
""")

# --- 3. Sleep Quality by Year of Study (Box Plot) ---
st.subheader("3. Sleep Quality (PSQI) by Year of Study")

fig_box = px.box(
    df,
    x='Year_of_Study',
    y='psqi_2_groups',
    color='Sex',
    points='all',  # show individual points
    color_discrete_sequence=px.colors.qualitative.Set2,
    title='Sleep Quality (PSQI) by Year of Study',
    labels={
        'Year_of_Study': 'Year of Study',
        'psqi_2_groups': 'PSQI Score (1 = Good, 2 = Poor)',
        'Sex': 'Gender'
    }
)

fig_box.update_layout(
    yaxis_title="PSQI Score (1 = Good, 2 = Poor)",
    xaxis_title="Year of Study",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=18),
    legend_title_text="Click to Filter by Gender"
)

st.plotly_chart(fig_box, use_container_width=True)

st.markdown("**Interpretation:**")
st.markdown("""
- Year 1 and 2 students have a mix of good and poor sleepers, while most Year 3 students tend to sleep better.  
- Sleep quality differences across years are small but noticeable.
""")
