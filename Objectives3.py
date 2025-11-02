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


# --- Scatter Plot: Anxiety vs Sleep Quality (Colored by Start Time) ---
if 'Start_time_code' in df.columns:
    st.subheader("Trait Anxiety vs Sleep Quality by Preferred Start Time")
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(7,5))
    sns.scatterplot(
        x='psqi_2_groups', 
        y='Trait_Anxiety', 
        hue='Start_time_code', 
        data=df, 
        palette='Spectral',
        ax=ax
    )
    ax.set_xlabel("Sleep Quality (PSQI)")
    ax.set_ylabel("Trait Anxiety")
    ax.set_title("Trait Anxiety vs Sleep Quality by Preferred Start Time")
    
    # Show the plot in Streamlit
    st.pyplot(fig)

# --- Correlation Heatmap ---
st.subheader("Correlation Heatmap")
# Use the exact 3 columns from your Colab
selected_cols = ['psqi_2_groups', 'Trait_Anxiety', 'MEQ']

# Compute correlation matrix
corr = df[selected_cols].corr()

# Plot same style as in Colab
fig, ax = plt.subplots(figsize=(7,5))
sns.heatmap(corr, annot=True, cmap='vlag', vmin=-1, vmax=1, ax=ax)
ax.set_title("Correlation Heatmap of Key Variables")

# Show in Streamlit
st.pyplot(fig)

st.markdown("""
*Interpretation:*  
This heatmap mirrors the Google Colab visualization.  
It shows correlation values among *Sleep Quality (PSQI), **Trait Anxiety, and **Chronotype (MEQ)*.  
Positive values (red) indicate that higher PSQI relates to higher anxiety,  
while negative values (blue) show inverse relationships.
""")
