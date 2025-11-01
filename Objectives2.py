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

st.success("✅ 'sleep_category' column created successfully!")

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

# --- Interaction Tip ---
st.markdown("💡 **Tip:** Hover over individual points to see exact anxiety scores. You can also zoom, pan, or export the graph.")

# ------------------------------------------------------------
# Step 3: Daytime Dozing Frequency by Sleep Quality Category
# ------------------------------------------------------------
plt.figure(figsize=(7, 5))
if 'Daytime_Dozing' in df.columns and 'sleep_category' in df.columns:
    doze_counts = pd.crosstab(df['sleep_category'], df['Daytime_Dozing'], normalize='index') * 100
    ax = doze_counts.plot(kind='bar', stacked=True, colormap='coolwarm', figsize=(7, 5))
    ax.set_title("Daytime Dozing Frequency by Sleep Quality Category")
    ax.set_xlabel("Sleep Category")
    ax.set_ylabel("Percentage (%)")
    ax.legend(title="Dozing Frequency", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(plt.gcf())
    st.markdown("""
    *Interpretation:*  
    The bar chart shows that poor sleepers experience *higher daytime dozing percentages* compared to good sleepers.  
    This pattern is consistent with the original Norbury & Evans (2018) results,  
    suggesting that insufficient nighttime sleep increases daytime drowsiness.
    """)
else:
    st.warning("⚠ Column 'Daytime_Dozing' or 'sleep_category' not found in dataset.")

# -----------------------------------------------------------
# Step 4: Chronotype (rMEQ Score) by Sleep Quality Category
# -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(7,4))
sns.violinplot(
    x='sleep_category',
    y='MEQ',
    data=df,
    palette='coolwarm',
    inner='quartile',
    ax=ax
)
ax.set_title("Chronotype (rMEQ Score) by Sleep Quality Category")
ax.set_xlabel("Sleep Category")
ax.set_ylabel("rMEQ Score (Higher = Morning Type)")
st.pyplot(fig)

st.markdown("""
*Interpretation:*  
This violin plot visualizes how chronotype (morningness–eveningness score) differs by sleep quality.  
Students with *poorer sleep* tend to show *lower rMEQ scores, indicating they are more **evening-type*.  
Those with *better sleep* usually score higher, showing stronger *morning preference*.
""")
