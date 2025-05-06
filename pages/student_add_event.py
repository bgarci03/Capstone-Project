import streamlit as st # type: ignore
from navigation import generate_sidebar

from connect import get_approved_signers_db

st.set_page_config(
  page_title="Remedy LOC Hours",
  page_icon=":material/list:",
  layout="wide"
)

try:
  if "roles" not in st.session_state or st.session_state.roles[0] != "student":
    st.switch_page("login.py")
except:
  st.switch_page("login.py")

generate_sidebar()

get_approved_signers_db()
signers = st.session_state.approved_signers_sheet.get_all_records()
signers_dict = dict()

for row in signers:
  signers_dict[row["Name"]] = [row["Email Address"], row["School"]]


st.title("Remedy Loss of Credit Hours", anchor=False)

form_container = st.container(border=True, key="remedy_form")
with form_container:
  time_started = st.time_input("**Time Started**", value=None, step=300)
  if time_started: st.write(f"*Selected Time in 12-hour format: {time_started.strftime("%I:%M %p")}*")
  
  time_ended = st.time_input("**Time Ended**", value=None, step=300)
  if time_ended: st.write(f"*Selected Time in 12-hour format: {time_ended.strftime("%I:%M %p")}*")

  date_completed = st.date_input("**Date Completed**", value=None, format="MM/DD/YYYY")
  if date_completed:
    date_phrase = date_completed.strftime("%A, %B %d, %Y")
    st.write(f"*Selected Date in Text: {date_phrase}*")
  
  approved_signer = st.selectbox("**Approved Signer**", list(signers_dict.keys()), placeholder="Choose an approved signer")
  if approved_signer:
    col1, col2 = st.columns(2)
    col1.write(f"*Email Address: {signers_dict[approved_signer][0]}*")
    col2.write(f"*School: {signers_dict[approved_signer][1]}*")


  with st.form("remedy_mini_form", clear_on_submit=True, border=False):
    hours_completed = st.number_input("**Hours Completed**", min_value=1, value=None)

    proof_of_completion = st.file_uploader("**Proof of Completion**", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button()
  
  inputs = (time_started, time_ended, date_completed, hours_completed, approved_signer, proof_of_completion)

  with st.empty():
    if submitted and None not in inputs:
      st.success("Form Submitted!")

      form_inputs = {
        "Time Started": time_started,
        "Time Ended": time_ended,
        "Date Completed": date_completed,
        "Approved Signer": approved_signer,
        "Hours Completed": hours_completed,
        "Proof of Completion": proof_of_completion
      }

    elif submitted and None in inputs:
      st.error("All fields must be filled!")
