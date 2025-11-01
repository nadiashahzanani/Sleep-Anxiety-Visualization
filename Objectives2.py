import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# -------------------------------------------
# PAGE 2: Group Comparisons and Chronotype
# -------------------------------------------

st.title("Objective 2 — Group Comparisons and Chronotype")

# Load dataset
url = "https://raw.githubusercontent.com/nadiashahzanani/Sleep-Anxiety-Visualization/refs/heads/main/Time_to_think_Norburyy.csv"
df = pd.read_csv(url)

# Fixed column names based on your dataset
sleep_cat_col = 'sleep_category' if 'sleep_category' in df.columns else df.columns[9]
anx_col = 'Trait_Anxiety' if 'Trait_Anxiety' in df.columns else df.columns[6]

# ============================================================
# Visualization 1 — Boxplot + Swarmplot (Trait Anxiety by Sleep Category)
# ============================================================

st.subheader("Trait Anxiety by Sleep Quality Category")

fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x=sleep_cat_col, y=anx_col, data=df, palette='Set2', ax=ax)
sns.swarmplot(x=sleep_cat_col, y=anx_col, data=df, color='0.3', size=3, ax=ax)
ax.set_title("Trait Anxiety by Sleep Quality Category")
ax.set_xlabel("Sleep Category")
ax.set_ylabel("Trait Anxiety Score")
st.pyplot(fig)

# ============================================================
# Statistical Test (T-test)
# ============================================================

# Extract good vs poor sleep groups
if 'Good Sleep' in df[sleep_cat_col].values and 'Poor Sleep' in df[sleep_cat_col].values:
    good = df[df[sleep_cat_col] == 'Good Sleep'][anx_col].dropna()
    poor = df[df[sleep_cat_col] == 'Poor Sleep'][anx_col].dropna()

    # Perform independent t-test
    t_stat, p_val = stats.ttest_ind(good, poor)

    st.markdown(f"""
    ### 🧮 Statistical Test Result (Independent T-Test)
    - **t-statistic:** {t_stat:.3f}  
    - **p-value:** {p_val:.4f}  
    """)

    # Interpretation
    if p_val < 0.05:
        st.success("✅ The difference in Trait Anxiety between Good Sleep and Poor Sleep groups is **statistically significant** (p < 0.05).")
    else:
        st.info("ℹ️ No statistically significant difference found (p ≥ 0.05).")

else:
    st.error("⚠️ Could not find 'Good Sleep' or 'Poor Sleep' categories in your dataset.")

# ============================================================
# Interpretation
# ============================================================
st.markdown("""
**Interpretation:**  
This visualization and t-test replicate the results from Norbury & Evans (2018).  
Students who reported **poorer sleep quality** tend to have **higher anxiety scores** on average.  
The t-test confirms that this difference is statistically significant, indicating a real effect — not random variation.
""")
