import streamlit as st # type: ignore

@st.cache_data
def get_sisd_disclaimer():
  with open("./media/sisd_disclaimer.txt") as file:
    return file.read()