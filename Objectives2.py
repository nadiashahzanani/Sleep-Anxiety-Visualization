import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px

st.title("1. Explore the relationship sleep quality, anxiety levels and daytime dozing")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# ------------------------------------------------------------
# Step 1: Create Sleep Category (Good vs Poor)
# ------------------------------------------------------------

# --- Ensure 'Chronotype' column exists ---
if 'Chronotype' not in df.columns:
    # Example thresholds for MEQ scores
    def categorize_meq(score):
        if score >= 60:
            return 'Morning Type
        elif score >= 40:
            return 'Intermediate Type'
        else:
            return 'Evening Type'
    df['Chronotype'] = df['MEQ'].apply(categorize_meq)

# --- Fit OLS regression ---
X = sm.add_constant(df['psqi_2_groups'])
y = df['Trait_Anxiety']
model = sm.OLS(y, X).fit()
r_squared = model.rsquared
p_value = model.pvalues[1]  # p-value for 'psqi_2_groups'

# --- Create Plotly scatter plot with regression line ---
fig = px.scatter(
    df,
    x='psqi_2_groups',
    y='Trait_Anxiety',
    color='Chronotype',
    trendline="ols",  # adds regression line automatically
    title=f"Sleep Quality vs Trait Anxiety (R² = {r_squared:.2f}, p = {p_value:.4f})",
    labels={'psqi_2_groups': 'PSQI (Sleep Quality)', 'Trait_Anxiety': 'Trait Anxiety'}
)

# --- Display the Plotly chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Optional Interpretation ---
st.markdown("Interpretation")
st.markdown("""
1. This scatter plot shows how sleep quality relates to trait anxiety, with colors representing different chronotypes.  
2. As sleep quality worsens, anxiety generally increases, and the regression line confirms this upward trend.  
3. Individual points reveal variation among chronotypes, indicating that chronotype may influence the relationship's strength or pattern.
    """)



# --- Statistical Test (t-test) ---
good = df[df['sleep_category']=='Good Sleep']['Trait_Anxiety']
poor = df[df['sleep_category']=='Poor Sleep']['Trait_Anxiety']
t, p = stats.ttest_ind(good, poor)
print(f"T-test result: t = {t:.3f}, p = {p:.4f}")

# ------------------------------------------------------------
# Step 3: Daytime Dozing Frequency by Sleep Quality Category
# ------------------------------------------------------------
# --- Check if 'Daytime_Dozing' column exists ---
if 'Daytime_Dozing' in df.columns and 'sleep_category' in df.columns:

    # --- Calculate normalized counts (percentage) ---
    doze_counts = (
        df.groupby('sleep_category')['Daytime_Dozing']
        .value_counts(normalize=True)
        .mul(100)
        .reset_index(name='Percentage')
    )

    # --- Create interactive stacked bar chart ---
    fig = px.bar(
        doze_counts,
        x='sleep_category',
        y='Percentage',
        color='Daytime_Dozing',
        title='Daytime Dozing Frequency by Sleep Quality Category',
        labels={
            'sleep_category': 'Sleep Category',
            'Daytime_Dozing': 'Dozing Frequency',
            'Percentage': 'Percentage (%)'
        },
        category_orders={
            "Daytime_Dozing": sorted(df['Daytime_Dozing'].dropna().unique())
        },
        text='Percentage'
    )

    # --- Enhance layout ---
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='inside')
    fig.update_layout(
        barmode='stack',
        yaxis_title="Percentage (%)",
        xaxis_title="Sleep Category",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend_title_text="Daytime Dozing Frequency",
        title_font=dict(size=18)
    )

    # --- Display interactive chart in Streamlit ---
    st.plotly_chart(fig, use_container_width=True)

    # --- Interpretation Section ---
    st.markdown("### **Interpretation:**")
    st.markdown("""
    1. The stacked bar chart shows the **percentage of students in each sleep quality category** (e.g., Good vs Poor sleepers) based on their **daytime dozing frequency**.  
    2. The color segments represent how often students doze during the day — lighter colors indicate less frequent dozing, while darker colors show more frequent dozing.  
    3. Students with **good sleep quality** generally show less variation in daytime dozing, suggesting they are more alert.  
    4. Poor sleepers, if present, may show higher daytime dozing percentages, reflecting lower alertness levels.
    """)

else:
    st.error("⚠️ Required column 'Daytime_Dozing' or 'sleep_category' not found in dataset.")

# -----------------------------------------------------------
# Step 4: Chronotype (rMEQ Score) by Sleep Quality Category
# -----------------------------------------------------------
# --- Create the interactive violin plot ---
st.subheader("1. Chronotype (rMEQ Score) by Sleep Quality Category (Interactive)")

fig = px.violin(
    df,
    x='sleep_category',
    y='MEQ',
    color='sleep_category',
    box=True,  # adds boxplot inside the violin
    points='all',  # show individual points
    title='Chronotype (rMEQ Score) by Sleep Quality Category',
    labels={
        'sleep_category': 'Sleep Category',
        'MEQ': 'rMEQ Score (Higher = Morning Type)'
    },
    color_discrete_sequence=px.colors.qualitative.Set2
)

# --- Improve layout and interaction ---
fig.update_layout(
    showlegend=False,  # no need for legend since color = x
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title_font=dict(size=18),
    xaxis_title='Sleep Quality Category',
    yaxis_title='rMEQ Score (Higher = Morning Type)',
)

# --- Add usage tip ---
st.markdown("💡 **Tip:** Hover over the violins or data points to see exact rMEQ scores interactively!")

# --- Display the Plotly chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("### **Interpretation:**")
st.markdown("""
1. This plot shows how being a *morning* or *evening* type (rMEQ score) relates to sleep quality.  
2. Among students with **good sleep**, most have mid-range rMEQ scores — meaning they’re neither extreme morning nor evening types.  
3. Some students with **poor sleep** lean toward eveningness (lower rMEQ scores).  
4. Overall, **good sleepers** include a mix of chronotypes, but slightly more lean toward morning types.
""")
