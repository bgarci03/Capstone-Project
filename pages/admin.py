import streamlit as st # type: ignore
from navigation import generate_sidebar

st.set_page_config(
  page_title="Admin Panel",
  layout="wide"
)

try:
  if "roles" not in st.session_state or st.session_state.roles[0] != "admin":
    st.switch_page("login.py")
except:
  st.switch_page("login.py")

generate_sidebar()

st.title("Admin Panel")

st.write(f"Welcome, {st.session_state.get("name")}! Manage Loss of Credit for students and view, add, or change events!")

st.write("Refresh the page to see new updated events!")