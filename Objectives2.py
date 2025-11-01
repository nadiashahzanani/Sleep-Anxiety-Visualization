import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px

st.title("Objective 2 — Group Comparisons and Chronotype")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# ------------------------------------------------------------
# Step 1: Create Sleep Category (Good vs Poor)
# ------------------------------------------------------------
if 'psqi_2_groups' in df.columns:
    df['sleep_category'] = np.where(df['psqi_2_groups'] <= 5, 'Good Sleep', 'Poor Sleep')
else:
    st.error("⚠ Column 'psqi_2_groups' not found in the dataset. Please check CSV structure.")
    st.stop()


# --- Interactive Box Plot using Plotly ---
st.subheader("1. Trait Anxiety by Sleep Quality Category (Interactive)")

fig = px.box(
    df,
    x='sleep_category',
    y='Trait_Anxiety',
    color='sleep_category',
    title='Trait Anxiety by Sleep Quality Category',
    labels={
        'sleep_category': 'Sleep Category',
        'Trait_Anxiety': 'Trait Anxiety Score'
    },
    hover_data=['Trait_Anxiety'],  # show details on hover
    color_discrete_sequence=px.colors.qualitative.Set2,
    points='all'  # show individual data points for transparency
)

# --- Customize layout for a cleaner look ---
fig.update_layout(
    yaxis_title="Trait Anxiety Score",
    xaxis_title="Sleep Category",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font=dict(size=18),
    showlegend=False
)

# --- Display interactive chart in Streamlit ---
st.plotly_chart(fig, use_container_width=True)

# --- Interpretation ---
st.markdown("### **Interpretation:**")
st.markdown("""
1. Students with **good sleep** tend to have moderate anxiety levels (around 45–50).  
2. Some good sleepers have **low anxiety** (25–30), while a few show **higher anxiety** (around 70).  
3. Students with **poor sleep** generally show a higher spread and slightly higher average anxiety.  
4. The wider box height indicates **greater variability** in anxiety among those with good sleep.
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
