# streamlit_app.py

import streamlit as st

login_page = st.Page("pages/entry_page.py", title="Login")

mvp_v1 = st.Page("pages/mvp.py", title="MVP V1")
if "password_correct" in st.session_state:
    pg = st.navigation(
        {
            "TOSAI MVP": [mvp_v1]
        }
    )

else:
    pg = st.navigation([login_page])

pg.run()



