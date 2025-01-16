import streamlit as st # type: ignore
import streamlit_authenticator as stauth # type: ignore

import yaml
from yaml.loader import SafeLoader

st.set_page_config(
  page_title="Login"
)

with open("./.streamlit/config.yaml") as file:
  config = yaml.load(file, Loader=SafeLoader)

st.session_state.authenticator = stauth.Authenticate(
  config['credentials'],
  config['cookie']['name'],
  config['cookie']['key'],
  config['cookie']['expiry_days']
)

st.title("Welcome")

try:
  st.session_state.authenticator.login()
except Exception as e:
  st.write("An error occured, please refresh the page!")

if st.session_state.get("authentication_status", None):
  role = st.session_state.get("roles")[0]

  try:
    st.switch_page(f"./pages/{role}.py")
  except:
    st.error(f"An error occured!")
    st.session_state["authentication_status"] = None

elif st.session_state.get("authentication_status", None) is False:
  st.error("Invalid Username/Password")

elif st.session_state.get("authentication_status", None) is None:
  st.error("Please enter your Username and Password")