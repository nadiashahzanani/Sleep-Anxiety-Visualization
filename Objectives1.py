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
