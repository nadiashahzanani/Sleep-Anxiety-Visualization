import streamlit as st

st.set_page_config(
    page_title="Student Survey"
)

page1 = st.Page('Objectives1.py', title='Pencapaian Akademik Pelajar', icon=":material/school:")
page2 = st.Page('Objectives2.py', title='Pencapaian Akademik Pelajar', icon=":material/school:")
page3 = st.Page('Objectives3.py', title='Pencapaian Akademik Pelajar', icon=":material/school:")

pg = st.navigation(
        {
            "Menu": [page1, page2, page3]
        }
    )

pg.run()
