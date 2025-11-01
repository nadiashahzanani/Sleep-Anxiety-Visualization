import pandas as pd
import plotly.express as px

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Now you can group or plot it safely
plot_df = df.groupby(['Year_of_Study', 'Sex']).size().unstack(fill_value=0)

# Create a grouped bar chart
fig = px.bar(
    df,
    x='Year_of_Study',
    color='Sex',
    barmode='group',
    title='Gender Distribution by Year of Study',
    labels={'Year_of_Study': 'Year of Study', 'Sex': 'Sex'}
)

fig.update_layout(yaxis_title="Number of Students")
fig.show()

# --- Interpretation ---
print("Interpretation:")
print("1. The chart shows that the number of students remains quite balanced across the different years of study.")
print("2. The color scale (Sex 1 and 2) indicates there are both male and female students in all years.")
print("3. However, the distribution looks slightly denser in the early years, suggesting more students in Year 1 or 2 compared to later years.")
