import streamlit as st # type: ignore
from navigation import generate_sidebar

st.set_page_config(
  page_title="Events",
  layout="wide"
)

generate_sidebar()

st.title("View and Change Events")