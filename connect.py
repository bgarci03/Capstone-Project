import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore

def get_student_loc_data_db():
  conn = st.connection("gsheets", type=GSheetsConnection)
  return conn.read(spreadsheet=st.secrets["database"]["students_url"], index_col="ID Number")

def get_approved_signers_db():
  conn = st.connection("gsheets", type=GSheetsConnection)
  return conn.read(spreadsheet=st.secrets["database"]["approved_signers_url"], index_col="Name")

def get_upcoming_loc_labs_db():
  conn = st.connection("ghseets", type=GSheetsConnection)
  return conn.read(spreadsheet=st.secrets["database"]["upcoming_loc_labs_url"], index_col="School")
