import streamlit as st # type: ignore
from streamlit.runtime.scriptrunner import get_script_run_ctx # type: ignore
from streamlit.source_util import get_pages # type: ignore

def get_current_page_name():
  ctx = get_script_run_ctx()
  if ctx is None:
    raise RuntimeError("Couldn't get script context")

  pages = get_pages("")

  return pages[ctx.active_script_hash]["page_name"]

def student_sidebar(role: str):
  st.page_link(f"./pages/{role}.py", label="Home")
  st.page_link(f"./pages/{role}_add_event.py", label="Add Event")
  st.page_link(f"./pages/{role}_upcoming_events.py", label="Upcoming Events")

def generate_sidebar():
  with st.sidebar:
    auth_status = st.session_state.get("authentication_status", False)

    if auth_status:
      role = st.session_state.get("roles")[0]
      
      st.title("SISD Loss of Credit")
      st.write(f"*{role.title()} View*")

      if role == "student":
        student_sidebar(role)
      
      st.session_state.authenticator.logout()

    elif get_current_page_name() != "login":
      st.switch_page("login.py")
