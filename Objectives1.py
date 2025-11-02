
import plotly.figure_factory as ff
import numpy as np

# Calculate mean and median for vertical lines
mean_psqi = df['psqi_2_groups'].mean()
median_psqi = df['psqi_2_groups'].median()

# Create distplot with custom bin_size
fig = ff.create_distplot([df['psqi_2_groups']], ['Distribution of Sleep Quality'], show_hist=True)

# Add vertical lines for mean and median
fig.add_shape(type="line", x0=mean_psqi, y0=0, x1=mean_psqi, y1=1,
              line=dict(color="red", width=2, dash="dash"),
              xref='x', yref='paper')
fig.add_annotation(x=mean_psqi, y=1, xref='x', yref='paper', text=f"Mean: {mean_psqi:.2f}", showarrow=False, yshift=10)

fig.add_shape(type="line", x0=median_psqi, y0=0, x1=median_psqi, y1=1,
              line=dict(color="green", width=2, dash="dash"),
              xref='x', yref='paper')
fig.add_annotation(x=median_psqi, y=1, xref='x', yref='paper', text=f"Median: {median_psqi:.2f}", showarrow=False, yshift=-10)


# Update layout for better readability
fig.update_layout(title_text='Distribution of Sleep Quality (PSQI) with Mean and Median',
                  xaxis_title='PSQI Score (Higher = Poorer Sleep)',
                  yaxis_title='Density')

fig.show()

# --- Interpretation ---
print("Interpretation:")
print("1. This plot shows how students’ sleep quality scores are spread out.")
print("2. Most students seem to have poorer sleep, with many scores clustering on the higher (worse) end—about half reported fairly or very bad sleep.")
