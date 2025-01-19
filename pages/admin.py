import streamlit as st # type: ignore
from navigation import generate_sidebar
from time import sleep

st.set_page_config(
  page_title="Admin Panel",
  layout="wide"
)

def welcome():
  msg = f"Welcome, {st.session_state.get("name")}! Manage Loss of Credit for students and view, add, or change events!"

  for char in msg:
    yield char
    sleep(0.02)

generate_sidebar()

st.title("Admin Panel")

st.write_stream(welcome)