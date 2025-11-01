# --- Import libraries ---
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page title ---
st.title("Interactive Visualization — Gender Distribution by Year of Study")

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
    title_x=0.5,
    legend_title="Click to Hide/Show Sex Group",
    plot_bgcolor='rgba(0,0,0,0)',
    hovermode="x unified"
)

# --- Display chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation section ---
st.subheader("Interpretation")

st.markdown("""
1. This chart displays **gender distribution** across different years of study.  
2. You can **click the legend labels (Sex 1 or Sex 2) to hide or show specific gender groups interactively.  
3. The hover tooltips show exact student counts per category.  
4. The overall distribution shows both male and female students in all study years, with slightly higher numbers in early years.
""")

# --- Interactive Plotly Histogram with Legend ---
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
1. Each color in the legend represents a PSQI sleep quality group — you can **click the legend items** to hide or show them interactively.  
2. Most students fall into two main groups — **good sleepers (PSQI = 1)** and **poor sleepers (PSQI = 2)**.  
3. The distribution is **bimodal**, meaning there are two peaks at PSQI = 1 and 2, showing that sleep quality tends to cluster into distinct categories.  
4. This interactive legend helps explore how different PSQI groups contribute to the overall pattern.
""")

# --- Interactive Box Plot with Legend Control ---
st.subheader("1. Sleep Quality (PSQI) by Year of Study (Interactive Legend)")

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
1. The chart is fully interactive — click the legend to isolate or compare genders.  
2. Students from Year 1 and Year 2 generally show a mix of good and poor sleepers (PSQI ≈ 1–2).  
3. Year 3 students mostly show better sleep (lower PSQI scores).  
4. The spread of data suggests sleep quality differences are small but noticeable across years.
""")
