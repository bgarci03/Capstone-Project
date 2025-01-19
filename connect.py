import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore

def get_student_loc_data_db():
  return st.connection("gsheets",type=GSheetsConnection).read(index_col="ID Number")