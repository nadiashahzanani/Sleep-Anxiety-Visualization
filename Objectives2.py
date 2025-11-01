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
# Step 2: Boxplot — Trait Anxiety by Sleep Category
# ------------------------------------------------------------
if 'Trait_Anxiety' in df.columns:
    fig, ax = plt.subplots(figsize=(6,4))
    sns.boxplot(x='sleep_category', y='Trait_Anxiety', data=df, palette='Set2', ax=ax)
    sns.swarmplot(x='sleep_category', y='Trait_Anxiety', data=df, color='0.3', size=3, ax=ax)
    ax.set_title("Trait Anxiety by Sleep Quality Category")
    ax.set_xlabel("Sleep Category")
    ax.set_ylabel("Trait Anxiety Score")
    st.pyplot(fig)

    # Optional statistical test
    good = df[df['sleep_category'] == 'Good Sleep']['Trait_Anxiety']
    poor = df[df['sleep_category'] == 'Poor Sleep']['Trait_Anxiety']
    t, p = stats.ttest_ind(good, poor, equal_var=False)
    st.write(f"**T-test Result:** t = {t:.2f}, p = {p:.4f}")

    st.markdown("""
    **Interpretation:**  
    The boxplot shows that students with **poor sleep quality** tend to have **higher trait anxiety** scores.  
    This pattern matches the Google Colab results — confirming a meaningful difference between Good and Poor Sleep groups.  
    """)
else:
    st.error("⚠️ Column 'Trait_Anxiety' not found in dataset.")
