# ===================================================
# Sleep, Anxiety & Start Time Visualization Homepage
# ===================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from scipy import stats
import numpy as np

# ------------------------------------------------------------
# Page Setup
# ------------------------------------------------------------
st.set_page_config(page_title="Sleep, Anxiety & Start Time Visualization", layout="wide")

# Header title
st.header("🧠 Time to Think — Sleep, Anxiety and University Start Time")

# Intro paragraph
st.write(
    """
    A scientific visualization exploring how **sleep quality**, **trait anxiety**, and **preferred class start times** interact among university students.
    """
)

# Dataset information
st.write(
    """
    This dashboard visualizes data from **Norbury & Evans (2018)** published in *Mendeley Data (V1)*.  
    The study explores psychological and behavioral patterns related to sleep, chronotype, and academic start times.
    """
)


page1 = st.Page('Objectives1.py', title='Distribution and Correlation', icon=":material/bar_chart:")

page2 = st.Page('Objectives2.py', title='Group Comparisons and Chronotype', icon=":material/groups:")

page3 = st.Page('Objectives3.py', title='Preferred Start Time & Correlation Matrix', icon=":material/timeline:")

pg = st.navigation(
        {
            "Menu": [page1, page2, page3]
        }
    )

pg.run()
