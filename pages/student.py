import streamlit as st # type: ignore
from navigation import generate_sidebar

from connect import get_student_loc_data_db

st.set_page_config(
  page_title="Home",
  page_icon=":material/home:",
  layout="wide"
)

try:
  if "roles" not in st.session_state or st.session_state.roles[0] != "student":
    st.switch_page("login.py")
except:
  st.switch_page("login.py")

student_data = get_student_loc_data_db().loc[int(st.session_state.get("id_number"))]

st.session_state.school = student_data.loc["School"]

generate_sidebar()

st.title("Your Loss of Credit", anchor=False)

hours_owed = student_data.loc["Hours Owed"]
if hours_owed > 0:
  if hours_owed <= 1:
    st.error(f"You owe {hours_owed} loss of credit hour!")
  else:
    st.error(f"You owe {hours_owed} loss of credit hours!")

hours_past_due = student_data.loc["Hours Past Due"]
if hours_past_due > 0:
  if hours_past_due <= 1:
    st.error(f"You have {hours_past_due} loss of credit hour past due!")
  else:
    st.error(f"You have {hours_past_due} loss of credit hours past due!")

top_container = st.container(border=True)
top_container.header("Student Information", divider="gray")

top_col1, top_col2, top_col3, top_col4 = top_container.columns(4)
top_col1.write(f"**ID Number:** {st.session_state.id_number}")
top_col2.write(f"**Student Name:** {st.session_state.name}")
top_col3.write(f"**Username:** {st.session_state.username}")
top_col4.write(f"**School:** {st.session_state.school}")

col1, col2, col3 = st.columns(3, border=True)
col1.header("Absences", divider="gray")
col1.write(f"**Current:** {student_data.loc["Absences"]}")
col2.header("Hours Owed", divider="gray")
col2.write(f"**Current:** {hours_owed}")
col3.header("Hours Past Due", divider="gray")
col3.write(f"**Current:** {hours_past_due}")
