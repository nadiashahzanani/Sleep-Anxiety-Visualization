# --- Import libraries ---
import streamlit as st
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# --- Page title ---
st.subheader("1. Gender Representation by Year Level")

# --- Load dataset ---
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Set the title for the Streamlit app
st.title("Arts Faculty Student Data")
col1, col2, col3, col4 = st.columns(4)

col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

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
    title_text="Distribution of Sleep Quality (PSQI) with Mean and Median",
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

# --- 2. Sleep Quality Distribution (Histogram) ---
st.title("2. Trait Anxiety by Year of Study")

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

# --- 3. Sleep Quality by Year of Study (Box Plot) ---
st.subheader("3. Sleep Quality Distribution by Sex")

 # Categorize psqi_2_groups into descriptive categories
def categorize_psqi(score):
    if score == 1:
        return 'Good Sleep'
    elif score == 2:
        return 'Poor Sleep'
    else:
        return 'Other'  # Handle unexpected values

df['Sleep_Quality_Category_Detailed'] = df['psqi_2_groups'].apply(categorize_psqi)

# Create grouped bar chart
    fig = px.bar(
        df,
        x='Sex',
        color='Sleep_Quality_Category_Detailed',
        barmode='group',
        title='Sleep Quality Category Distribution by Sex',
        labels={'Sex': 'Sex', 'Sleep_Quality_Category_Detailed': 'Sleep Quality Category'}
    )

    fig.update_layout(yaxis_title="Number of Students")
    
    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Add interpretation
    st.subheader("Interpretation")
    st.markdown("""
    1. This grouped bar chart compares how sleep quality levels differ between male and female students.  
    2. It shows which gender reports better or poorer sleep more often, helping us see if one group tends to struggle more with sleep quality.
    """)
else:
    st.info("Please upload a CSV file to visualize the data.")
