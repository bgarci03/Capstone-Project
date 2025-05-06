import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore

import gspread # type: ignore
from oauth2client.service_account import ServiceAccountCredentials # type: ignore

# Google Sheets Authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

def get_student_loc_data_db():
  st.session_state.student_loc_sheet = client.open("Secure_Students").sheet1

def get_approved_signers_db():
  st.session_state.approved_signers_sheet = client.open("Secure_Approved_Signers").sheet1

def get_upcoming_loc_labs_db():
  st.session_state.upcoming_loc_sheet = client.open("Secure_Upcoming_LOC_Labs").sheet1
