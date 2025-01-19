import streamlit as st # type: ignore
from time import sleep
from navigation import generate_sidebar

st.set_page_config(
  page_title="Remedy LOC Hours",
  layout="wide"
)

generate_sidebar()

st.title("Remedy Loss of Credit Hours", anchor=False)

form_container = st.container(border=True, key="remedy_form")
with form_container:
  time_started = st.time_input("**Time Started**", value=None)
  if time_started: st.write(f"*Selected Time in 12-hour format: {time_started.strftime("%I:%M %p")}*")
  
  time_ended = st.time_input("**Time Ended**", value=None)
  if time_ended: st.write(f"*Selected Time in 12-hour format: {time_ended.strftime("%I:%M %p")}*")

  date_completed = st.date_input("**Date Completed**", value=None, format="MM/DD/YYYY")
  if date_completed:
    date_phrase = date_completed.strftime("%A, %B %d, %Y")
    st.write(f"*{date_phrase}*")


  with st.form("remedy_mini_form", border=False):
    hours_completed = st.number_input("**Hours Completed**", min_value=1, value=None)

    approved_signer = st.text_input("**Approved Signer**")

    proof_of_completion = st.file_uploader("**Proof of Completion**", type=["pdf", "png", "jpg", "jpeg"])

    submitted = st.form_submit_button()
  
  inputs = (time_started, time_ended, date_completed, hours_completed, approved_signer, proof_of_completion)

  with st.empty():
    if submitted and None not in inputs:
      st.success("Form Submitted!")
    elif submitted and None in inputs:
      st.error("All fields must be filled!")
