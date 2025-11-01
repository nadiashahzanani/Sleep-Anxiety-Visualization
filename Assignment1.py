import streamlit as st

st.set_page_config(
    page_title="Sleep, Anxiety & Start Time Visualization App"
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
