import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Objectives 3 - Start-Time Preferences, Chronotype and Sleep Quality in Policy Implications")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Ensure 'Chronotype' column exists
if 'Chronotype' not in df.columns:
    # Categorize MEQ scores into Chronotypes
    def categorize_meq(score):
        if score >= 60:
            return 'Morning Type'
        elif score >= 40:
            return 'Intermediate Type'
        else:
            return 'Evening Type'
    
    df['Chronotype'] = df['MEQ'].apply(categorize_meq)

# Now calculate chronotype counts safely
chronotype_counts = df['Chronotype'].value_counts()

# --- Calculate summary metrics for Objective 3 ---
mean_pref_start = df['Start_time_code'].mean()
mean_sleep_quality = df['psqi_2_groups'].mean()
chronotype_counts = df['Chronotype'].value_counts() if 'Chronotype' in df.columns else df['MEQ'].apply(categorize_meq).value_counts()
earliest_start = df['Start_time_code'].min()
latest_start = df['Start_time_code'].max()


# Set the title for the Streamlit app
st.subheader("Start Time Preferences & Chronotype")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="Avg Preferred Start Time", value=f"{mean_pref_start:.2f} h",
            help="Average hour students prefer to start classes")
col2.metric(label="Avg Sleep Quality", value=f"{mean_sleep_quality:.2f}",
            help="Higher value indicates poorer sleep quality")
col3.metric(label="Earliest Preferred Start", value=f"{earliest_start:.2f} h",
            help="Earliest hour preferred by any student")
col4.metric(label="Latest Preferred Start", value=f"{latest_start:.2f} h",
            help="Latest hour preferred by any student")

st.title("3.1. Distribution of Prefereed Class Start Time Across Chronotypes")

# Create interactive violin plot with Plotly
fig = px.violin(
    df,
    x='Chronotype',
    y='Start_time_code',  # Replace with your column for preferred start time
    box=True,  # adds boxplot inside violin
    points='all',  # show all individual data points
    title='- Preferred Start Time by Chronotype',
    labels={'Chronotype': 'Chronotype', 'Start_time_code': 'Preferred Start Time'}
)

# Display plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add interpretation
st.subheader("Interpretation")
st.markdown("""
1. This violin plot shows how students with different chronotypes prefer different class start times.  
2. Evening types generally prefer starting later than morning types, and their preferences vary more widely.
""")


st.title("3.2. How Sleep Quality Varies With Preferred Start Times")

# Create the Plotly density heatmap
fig = px.density_heatmap(
    df,
    x='Start_time_code',
    y='psqi_2_groups',
    title=' - Preferred Start Time vs Sleep Quality',
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

st.title("3.3. Average Gap Between Preferred and Actual Start Times by Year (With Sleep Quality)")
    
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
    title=' - Mean Preferred Start Time by Year of Study',
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
st.subheader("Interpretation")
st.markdown("""
1. This chart shows how students in each year prefer different class start times 
    and how their average sleep quality compares. 
2. Years that prefer later starts but report poorer sleep may benefit from adjusted schedules.
""")
st.plotly_chart(fig, use_container_width=True)
