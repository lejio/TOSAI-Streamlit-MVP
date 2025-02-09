# streamlit_app.py

import streamlit as st
from components.auth import check_password

st.write("TOSAI")

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

st.write("Hello World!")
st.button("Test button")