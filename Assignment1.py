
import streamlit as st

st.set_page_config(
    page_title="Sleep, Anxiety & Start Time Visualization"
)

home = st.Page('home.py', title='Home', icon=":material/school:")

page1 = st.Page('Objectives1.py', title='Page 1', icon=":material/bar_chart:")

page2 = st.Page('Objectives2.py', title='Page 2', icon=":material/groups:")

page3 = st.Page('Objectives3.py', title='Page 3', icon=":material/timeline:")

pg = st.navigation(
        {
            "Menu": [home, page1, page2, page3]
        }
    )

pg.run()
