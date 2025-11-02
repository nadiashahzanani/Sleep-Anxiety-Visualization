# --- Import libraries ---
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as pd
import pandas as pd

# --- Page title ---
st.subheader("Objectives 1: Sleep and Anxiety Levels Across Different Groups")

# --- Load dataset ---
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Calculate mean and median
mean_psqi = df['psqi_2_groups'].mean()
median_psqi = df['psqi_2_groups'].median()

# Create Plotly distplot
fig = ff.create_distplot(
    [df['psqi_2_groups'].dropna()],
    group_labels=['Distribution of Sleep Quality'],
    show_hist=True,
    show_rug=False
)

# Add mean and median lines
fig.add_shape(
    type="line",
    x0=mean_psqi, y0=0,
    x1=mean_psqi, y1=1,
    line=dict(color="red", width=2, dash="dash"),
    xref='x', yref='paper'
)
fig.add_annotation(
    x=mean_psqi, y=1,
    xref='x', yref='paper',
    text=f"Mean: {mean_psqi:.2f}",
    showarrow=False, yshift=10,
    font=dict(color="red")
)

fig.add_shape(
    type="line",
    x0=median_psqi, y0=0,
    x1=median_psqi, y1=1,
    line=dict(color="green", width=2, dash="dash"),
    xref='x', yref='paper'
)
fig.add_annotation(
    x=median_psqi, y=1,
    xref='x', yref='paper',
    text=f"Median: {median_psqi:.2f}",
    showarrow=False, yshift=-10,
    font=dict(color="green")
)

# Layout updates
fig.update_layout(
    title_text="1. Distribution of Sleep Quality (PSQI) with Mean and Median",
    xaxis_title="PSQI Score (Higher = Poorer Sleep)",
    yaxis_title="Density",
    template="plotly_white",
    width=800,
    height=500
)

# Display the figure inside Streamlit
st.plotly_chart(fig, use_container_width=True)

# --- Simple interpretation (Streamlit text output) ---
st.markdown("Interpretation")
st.write("""
This plot shows how students’ sleep quality scores are spread out. 
Most students appear to have poorer sleep, with many scores clustering toward the higher (worse) end — 
about half reported fairly or very bad sleep.
""")



# --- Interactive Plotly Histogram with Legend ---
st.subheader("2. Trait Anxiety by Year of Study")

# Create Plotly boxplot
fig = px.box(
    df,
    x='Year_of_Study',
    y='Trait_Anxiety',
    points='all',  # Show all points
    title='Trait Anxiety by Year of Study',
    labels={'Year_of_Study': 'Year of Study', 'Trait_Anxiety': 'Trait Anxiety Score'},
    color='Year_of_Study'  # Optional: color by year for better distinction
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("Interpretation")
st.write("""
1. This boxplot shows how students’ anxiety levels differ across their years of study.  
2. Overall, first-year students tend to have slightly higher and more varied anxiety scores, suggesting they may feel more stress as they adjust to university life.
""")

# --- Interactive Box Plot with Legend Control ---
st.subheader("3. Sleep Quality (PSQI) by Year of Study (Interactive Legend)")

fig = px.box(
    df,
    x='Year_of_Study',
    y='psqi_2_groups',
    color='Sex',
    title='Sleep Quality (PSQI) by Year of Study',
    labels={
        'Year_of_Study': 'Year of Study',
        'psqi_2_groups': 'PSQI Score (1 = Good, 2 = Poor)',
        'Sex': 'Gender'
    },
    points='all',  # show individual data points
    color_discrete_sequence=px.colors.qualitative.Set2
)

# --- Improve Layout & Interactivity ---
fig.update_layout(
    yaxis_title="PSQI Score (1 = Good, 2 = Poor)",
    xaxis_title="Year of Study",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=18),
    legend_title_text="Click to Filter by Gender",  # encourage legend interaction
)

# --- Display interactive chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("### *Interpretation:*")
st.markdown("""
1. This chart shows that students in Year 1 and 2 have a mix of good and poor sleepers, while most Year 3 students tend to sleep better. 
2. Overall, sleep quality differences across years are small but still noticeable.
""")
