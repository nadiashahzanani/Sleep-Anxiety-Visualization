import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np # Needed for bar position calculation

# --- Assuming 'df' is your pandas DataFrame loaded earlier in the script ---

# 1. Prepare Data for Matplotlib (Group and Count)
# This mimics the aggregation performed implicitly by px.bar
plot_df = df.groupby(['Year_of_Study', 'Sex']).size().unstack(fill_value=0)

# 2. Create Matplotlib Figure
# Create a figure and an axis object
fig, ax = plt.subplots(figsize=(10, 6))

# Define bar width and positions
bar_width = 0.35
# Get the positions of the 'Year_of_Study' categories on the x-axis
x = np.arange(len(plot_df.index)) 

# Plot the bars for each 'Sex' category
# 'Sex' 1 bars will be slightly to the left, 'Sex' 2 bars slightly to the right
rects1 = ax.bar(x - bar_width/2, plot_df.iloc[:, 0], bar_width, label=plot_df.columns[0])
rects2 = ax.bar(x + bar_width/2, plot_df.iloc[:, 1], bar_width, label=plot_df.columns[1])

# Add labels, title, and custom x-axis tick labels
ax.set_title('Gender Distribution by Year of Study')
ax.set_xlabel('Year of Study')
ax.set_ylabel('Number of Students')

# Set x-axis ticks to be the actual 'Year_of_Study' values
ax.set_xticks(x)
ax.set_xticklabels(plot_df.index)

# Add a legend
ax.legend(title='Sex')

# Ensure layout is tight to prevent labels from being cut off
plt.tight_layout()

# 3. Display the Matplotlib figure in Streamlit
st.pyplot(fig)

# --- Interpretation (for display in Streamlit) ---
st.subheader("Interpretation:")
st.write("1. The chart shows that the number of students remains quite balanced across the different years of study.")
st.write("2. The color scale (Sex 1 and 2) indicates there are both male and female students in all years.")
st.write("3. However, the distribution looks slightly denser in the early years, suggesting more students in Year 1 or 2 compared to later years.")
