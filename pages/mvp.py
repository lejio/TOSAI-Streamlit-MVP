import streamlit as st

st.title("TOSAI MVP 1")

input_col, pref_col = st.columns(2, gap='large')

with input_col:
    txt = st.text_area("Paste legal document", height=500)

st.divider()

with pref_col:
    pref_tree = st.text_area("Edit your preference", height=500)

st.write("## Output")