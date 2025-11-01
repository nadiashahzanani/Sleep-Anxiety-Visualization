import streamlit as st

st.set_page_config(
    page_title="Sleep, Anxiety & Start Time Visualization App"
)

page1 = st.Page('Objectives1.py', title='Distribution and Correlation', icon=":material/school:")
page2 = st.Page('Objectives2.py', title='Group Comparisons and Chronotype', icon=":material/school:")
page3 = st.Page('Objectives3.py', title='Preferred Start Time & Correlation Matrix', icon=":material/school:")

pg = st.navigation(
        {
            "Menu": [page1, page2, page3]
        }
    )

pg.run()
