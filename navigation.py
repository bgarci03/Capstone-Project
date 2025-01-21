import streamlit as st # type: ignore
from streamlit.runtime.scriptrunner import get_script_run_ctx # type: ignore
from streamlit.source_util import get_pages # type: ignore

from disclaimer import get_sisd_disclaimer

# Match Page
def get_current_page_name():
  ctx = get_script_run_ctx()
  if ctx is None:
    raise RuntimeError("Couldn't get script context")

  pages = get_pages("")

  return pages[ctx.active_script_hash]["page_name"]

# Student Functions
def student_sidebar():
  st.page_link("./pages/student.py", label="Home")
  st.page_link("./pages/student_add_event.py", label="Remedy LOC Hours")
  st.page_link("./pages/student_upcoming_events.py", label="Upcoming LOC Labs")

# Admin Functions
def admin_sidebar():
  st.page_link("./pages/admin.py", label="Panel")
  st.page_link("./pages/admin_events.py", label="Events")

# Sidebar Generation
def generate_sidebar():
  with st.sidebar:
    auth_status = st.session_state.get("authentication_status", False)

    if auth_status:
      role = st.session_state.get("roles")[0]

      st.logo("./media/SISD_Seal.jpeg")

      st.title("SISD Loss of Credit")
      st.write(f"*{role.title()} View*")

      st.write(f"**{st.session_state.get("name")}**")

      if role == "student":
        student_sidebar()
      
      elif role == "admin":
        admin_sidebar()
      
      st.session_state.authenticator.logout()

    elif get_current_page_name() != "login":
      st.switch_page("login.py")
