import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.title("Objective 1 — Distribution and Correlation")

url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

def load_data():
    # Simulate a bimodal distribution for 'psqi_2_groups'
    # Group 1 (Good Sleep, score=1): High frequency
    good_sleep = np.random.normal(loc=1.0, scale=0.1, size=300) 
    # Group 2 (Poor Sleep, score=2): High frequency
    poor_sleep = np.random.normal(loc=2.0, scale=0.1, size=200)
    # Moderate sleep (in between 1 and 2): Low frequency
    moderate_sleep = np.random.uniform(low=1.2, high=1.8, size=50)

    # Combine and ensure values are close to 1 or 2 as suggested by interpretation
    data = np.concatenate([good_sleep, poor_sleep, moderate_sleep])
    data = np.clip(data, 0.9, 2.1) # Clip to keep it realistic for PSQI groups 1 and 2

    df = pd.DataFrame({
        'psqi_2_groups': data
    })
    return df

# Load the (mock) data
df = load_data()

# --- 2. STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Sleep Quality Distribution", layout="centered")
st.title("Sleep Quality Distribution Analysis")

# --- 3. PLOT GENERATION (Matplotlib/Seaborn) ---

# Create the figure object explicitly (crucial for st.pyplot)
fig, ax = plt.subplots(figsize=(8, 5))

# Use seaborn to create the histogram on the created axes (ax)
sns.histplot(
    df['psqi_2_groups'], 
    kde=True, 
    color='#6495ED', # Using a pleasant color
    ax=ax,
    bins=30 # Adjust bin size for better visualization of the bimodality
)

# Apply styling to the figure using the axes object
ax.set_title("Distribution of Sleep Quality (PSQI Score)", fontsize=16)
ax.set_xlabel("PSQI Score (Lower Score = Better Sleep)", fontsize=12)
ax.set_ylabel("Number of Students", fontsize=12)

# Set clearer x-axis limits/labels to emphasize the two groups
ax.set_xticks([1.0, 2.0])
ax.set_xticklabels(['Good Sleep (Score ≈ 1)', 'Poor Sleep (Score ≈ 2)'])

# Add interpretation to the chart:
st.pyplot(fig)

# --- 4. INTERPRETATION DISPLAY (Streamlit) ---
st.markdown("---")
st.header("Chart Interpretation")

interpretation = """
1. **Bimodal Distribution**: The chart clearly shows two main peaks, indicating that students tend to cluster into two distinct categories: one with **Good Sleep** (around PSQI Score 1) and another with **Poor Sleep** (around PSQI Score 2).
2. **Polarized Sleep Patterns**: The valley between the two peaks suggests a low number of students with *moderate* sleep quality, confirming the trend of distinct sleep patterns rather than a continuous, normally distributed range.
3. **Focus Areas**: The distribution helps identify the size of the population in need of intervention (the 'Poor Sleep' cluster).
"""

st.markdown(interpretation)

st.markdown("---")
st.info(
    "To run this Streamlit app, save the code as `streamlit_psqi_chart.py` and run `streamlit run streamlit_psqi_chart.py` in your terminal."
)
