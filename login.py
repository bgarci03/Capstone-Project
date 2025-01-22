import streamlit as st # type: ignore
import streamlit_authenticator as stauth # type: ignore

from disclaimer import get_sisd_disclaimer

import yaml
from yaml.loader import SafeLoader

st.set_page_config(
  page_title="Login"
)

def add_student_info():
  with open("./.streamlit/config.yaml", "r") as file:
    config = yaml.load(file, Loader=SafeLoader)
  
  username = st.session_state.get("username")
  st.session_state["id_number"] = config["credentials"]["usernames"][username].get("id_number")

with open("./.streamlit/config.yaml") as file:
  config = yaml.load(file, Loader=SafeLoader)

try:
  for key in st.session_state.keys():
    del st.session_state.key
except:
  pass

st.session_state.authenticator = stauth.Authenticate(
  config['credentials'],
  config['cookie']['name'],
  config['cookie']['key'],
  config['cookie']['expiry_days']
)

st.logo("./media/SISD_Seal.png")

st.title("SISD Loss of Credit")

try:
  st.session_state.authenticator.login()
except Exception as e:
  st.write("An error occured! Please refresh the page!")

if st.session_state.get("authentication_status", None):
  role = st.session_state.get("roles")[0]

  try:
    if role == "student":
      add_student_info()

    st.switch_page(f"./pages/{role}.py")
  except Exception as e:
    st.error(f"An error occured! Please restart your browser!")
    st.session_state["authentication_status"] = None

elif st.session_state.get("authentication_status", None) is False:
  st.error("Invalid Username/Password")

elif st.session_state.get("authentication_status", None) is None:
  st.info("Please enter your Username and Password")

st.divider()
st.write(get_sisd_disclaimer())