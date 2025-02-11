import streamlit as st
from components.auth import check_password

st.title("TOSAI")

if not check_password():
    st.stop()  # Do not continue if check_password is not True.