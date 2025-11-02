# Streamlit header
st.subheader("Distribution of Sleep Quality (PSQI)")

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
