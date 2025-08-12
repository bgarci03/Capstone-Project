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
st.write("You can view every loss of credit lab/event in the **Manage Events** page in the sidebar with the Calendar!")

col1, col2 = st.columns(2, border=True)

with col1:
  st.header("How to add an event!")
  st.markdown(
  """
  1. *Head* to the page **Managed Events**
  2. *Select* the **Add Event** tab at the top
  3. *Fill out* the form
  4. **Submit** the form
  """)

with col2:
  st.header("How to delete an event!")
  st.markdown(
  """
  1. *Head* to the page **Managed Events**
  2. *Select* the **Delete Event** tab at the top
  3. *Fill out* the first two inputs
  4. *Look* for the event to delete
  5. *Copy* the event information
  6. **Submit** the form
  """)
