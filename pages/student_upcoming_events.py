import streamlit as st # type: ignore
from navigation import generate_sidebar

st.set_page_config(
  page_title="Upcoming Events",
  layout="wide"
)

generate_sidebar()

st.title("Upcoming Events", anchor=False)
