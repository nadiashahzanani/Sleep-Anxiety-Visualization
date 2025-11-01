import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title("Objective 3 — Preferred Start Time & Correlation Matrix")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# --- Check if column exists ---
if 'Start_time_code' in df.columns and 'sleep_category' in df.columns:
    
    st.subheader("1. Preferred University Start Time by Sleep Category (Interactive)")

    # --- Plotly Interactive Bar Chart ---
    fig = px.bar(
        df,
        x='Start_time_code',
        color='sleep_category',
        title='Preferred University Start Time by Sleep Category',
        labels={
            'Start_time_code': 'Preferred Start Time Code',
            'sleep_category': 'Sleep Category'
        },
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # --- Improve layout for clarity ---
    fig.update_layout(
        xaxis_title="Preferred Start Time Code",
        yaxis_title="Number of Students",
        legend_title="Sleep Category",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_font=dict(size=18),
        legend=dict(title_font=dict(size=12))
    )

    # --- Add interactive legend note ---
    st.markdown("💡 **Tip:** Click the legend items to hide or show each sleep category interactively.")

    # --- Display interactive chart ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Interpretation ---
    st.markdown("### **Interpretation:**")
    st.markdown("""
    1. The chart shows when students with good vs. poor sleep prefer classes to start.  
    2. Most **good sleepers** prefer class start times around **code 5–6**, likely corresponding to mid-morning (≈ 9–10 AM).  
    3. Fewer students prefer very early (code 3–4) or very late (code 8–9) start times.  
    4. This suggests that **good sleepers tend to favor moderate start times**, not too early or too late.
    """)
else:
    st.warning("⚠️ Column related to preferred start time or sleep category not found in the dataset.")



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
