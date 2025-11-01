import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
    st.error("⚠️ Column 'psqi_2_groups' not found in the dataset. Please check CSV structure.")
    st.stop()

st.success("✅ 'sleep_category' column created successfully!")

 # ------------------------------------------------------------
    # Step 2: Boxplot — Trait Anxiety by Sleep Category (Plotly)
    # ------------------------------------------------------------
    if 'Trait_Anxiety' in df.columns and 'sleep_category' in df.columns:
        fig = px.box(
            df,
            x='sleep_category',
            y='Trait_Anxiety',
            title='Trait Anxiety by Sleep Quality Category',
            labels={
                'sleep_category': 'Sleep Category',
                'Trait_Anxiety': 'Trait Anxiety Score'
            },
            hover_data=['Trait_Anxiety'],
            color='sleep_category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        # Display interactive plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # ------------------------------------------------------------
        # Statistical Test (T-test)
        # ------------------------------------------------------------
        if 'Good Sleep' in df['sleep_category'].unique() and 'Poor Sleep' in df['sleep_category'].unique():
            good = df[df['sleep_category'] == 'Good Sleep']['Trait_Anxiety']
            poor = df[df['sleep_category'] == 'Poor Sleep']['Trait_Anxiety']
            t, p = stats.ttest_ind(good, poor, equal_var=False)

            st.markdown(f"**T-test Result:**  t = `{t:.2f}`,  p = `{p:.4f}`")

            # ------------------------------------------------------------
            # Interpretation
            # ------------------------------------------------------------
            st.markdown("""
            ### 🧠 Interpretation  
            1. Students with **poor sleep quality** tend to have **higher trait anxiety** scores.  
            2. Those with **good sleep** generally show **lower anxiety levels** (around mid-range values 45–50).  
            3. There’s still some variation, suggesting other factors may also affect anxiety.  
            
            ✅ This matches the observed pattern in your Google Colab results — confirming a meaningful difference between Good and Poor Sleep groups.
            """)
        else:
            st.warning("⚠️ Both 'Good Sleep' and 'Poor Sleep' categories are required for the t-test.")
    else:
        st.error("⚠️ Columns 'Trait_Anxiety' and/or 'sleep_category' not found in dataset.")

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
    **Interpretation:**  
    The bar chart shows that *poor sleepers* experience **higher daytime dozing percentages** compared to good sleepers.  
    This pattern is consistent with the original Norbury & Evans (2018) results,  
    suggesting that insufficient nighttime sleep increases daytime drowsiness.
    """)
else:
    st.warning("⚠️ Column 'Daytime_Dozing' or 'sleep_category' not found in dataset.")

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
**Interpretation:**  
This violin plot visualizes how chronotype (morningness–eveningness score) differs by sleep quality.  
Students with **poorer sleep** tend to show **lower rMEQ scores**, indicating they are more **evening-type**.  
Those with **better sleep** usually score higher, showing stronger **morning preference**.
""")
