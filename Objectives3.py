import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Objective 3 — Preferred Start Time by Chronotype")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Ensure 'Chronotype' column exists
if 'Chronotype' not in df.columns:
    # Categorize MEQ scores into Chronotypes (adjust thresholds as needed)
    def categorize_meq(score):
        if score >= 60:
            return 'Morning Type'
        elif score >= 40:
            return 'Intermediate Type'
        else:
            return 'Evening Type'
    df['Chronotype'] = df['MEQ'].apply(categorize_meq)

# Create interactive violin plot with Plotly
fig = px.violin(
    df,
    x='Chronotype',
    y='Start_time_code',  # Replace with your column for preferred start time
    box=True,  # adds boxplot inside violin
    points='all',  # show all individual data points
    title='Preferred Start Time by Chronotype',
    labels={'Chronotype': 'Chronotype', 'Start_time_code': 'Preferred Start Time'}
)

# Display plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add interpretation
st.markdown("Interpretation")
st.markdown("""
1. This violin plot shows how students with different chronotypes prefer different class start times.  
2. Evening types generally prefer starting later than morning types, and their preferences vary more widely.
""")


st.title("2. Preferred Start Time vs Sleep Quality")

# Create the Plotly density heatmap
fig = px.density_heatmap(
    df,
    x='Start_time_code',
    y='psqi_2_groups',
    title='Preferred Start Time vs Sleep Quality',
    labels={
        'Start_time_code': 'Preferred Start Time Code',
        'psqi_2_groups': 'PSQI (Sleep Quality)'
    },
    color_continuous_scale='Blues'
)

# Display the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Interpretation
st.subheader("Interpretation")
st.markdown("""
1. This heatmap shows where most students fall based on their preferred class start time and sleep quality.  
2. Darker areas toward the top-right indicate many poor sleepers prefer later class times, suggesting that starting classes later might help improve their sleep.
""")

# --- Scatter Plot: Anxiety vs Sleep Quality (Colored by Start Time) ---
if 'Start_time_code' in df.columns:
    st.subheader("Trait Anxiety vs Sleep Quality by Preferred Start Time")
    
# --- Calculate mean preferred start time and mean sleep quality by Year of Study ---
mean_start_time_quality = df.groupby('Year_of_Study').agg(
    Mean_Start_Time_Code=('Start_time_code', 'mean'),
    Mean_Sleep_Quality=('psqi_2_groups', 'mean')
).reset_index()

# --- Create Plotly bar chart ---
fig = px.bar(
    mean_start_time_quality,
    x='Year_of_Study',
    y='Mean_Start_Time_Code',
    title='Mean Preferred Start Time by Year of Study',
    labels={'Year_of_Study': 'Year of Study', 'Mean_Start_Time_Code': 'Mean Preferred Start Time Code'},
    text='Mean_Start_Time_Code',  # optional: show bar values
    color='Mean_Start_Time_Code',  # optional: color by height
    color_continuous_scale='Blues'
)

# Add annotations for mean sleep quality
for index, row in mean_start_time_quality.iterrows():
    fig.add_annotation(
        x=row['Year_of_Study'],
        y=row['Mean_Start_Time_Code'],
        text=f"Sleep Quality: {row['Mean_Sleep_Quality']:.2f}",
        showarrow=False,
        yshift=10
    )

# --- Interpretation ---
st.markdown("Interpretation")
st.markdown("""
1. This chart shows how students in each year prefer different class start times 
    and how their average sleep quality compares. 
2. Years that prefer later starts but report poorer sleep may benefit from adjusted schedules.
""")
st.plotly_chart(fig, use_container_width=True)
