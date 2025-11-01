# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page title ---
st.subheader("1. Gender Representation by Year Level")

# --- Load dataset ---
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Create interactive Plotly bar chart (interactive legend built-in) ---
fig = px.bar(
    df,
    x='Year_of_Study',
    color='Sex',
    barmode='group',
    title='Gender Distribution by Year of Study',
    labels={'Year_of_Study': 'Year of Study', 'Sex': 'Sex'},
)

# --- Customize layout ---
fig.update_layout(
    yaxis_title="Number of Students",
    xaxis_title="Year of Study",
    title_x=0.3,
    legend_title="Click to Hide/Show Sex Group",
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode="x unified"
)

# --- Display chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation section ---
st.subheader("Interpretation:")

st.markdown("""
1. This chart shows the gender distribution across different years of study.
2. It reveals that both male and female students are present in every year, with slightly more students in the earlier years.
""")


# --- Interactive Plotly Histogram with Legend ---
st.subheader("2. Basic Sleep Quality Distribution")

fig = px.histogram(
    df,
    x='psqi_2_groups',
    color='psqi_2_groups',  # adds interactive legend by grouping color
    nbins=10,
    color_discrete_sequence=px.colors.qualitative.Set2,
    title="Distribution of Sleep Quality (PSQI)",
)

fig.update_layout(
    xaxis_title="PSQI Score (Higher = Poorer Sleep)",
    yaxis_title="Number of Students",
    bargap=0.1,
    template="simple_white",
    legend_title_text="PSQI Group",
)

# --- Enable interactive legend behavior ---
# (Plotly does this by default — users can click legend items to hide/show)
fig.update_traces(opacity=0.8)

# --- Display chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("### **Interpretation:**")
st.markdown("""
1. Most students are grouped into two main sleep quality categories which is good sleepers (PSQI = 1) and poor sleepers (PSQI = 2).
2. The interactive legend allows users to easily explore how each group contributes to the overall sleep pattern.
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

# --- Add helpful instructions ---
st.markdown("💡 **Tip:** Click on the legend items (e.g., *Male*, *Female*) to hide or show them interactively!")

# --- Display interactive chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("### **Interpretation:**")
st.markdown("""
1. This chart shows that students in Year 1 and 2 have a mix of good and poor sleepers, while most Year 3 students tend to sleep better. 
2. Overall, sleep quality differences across years are small but still noticeable.
""")
