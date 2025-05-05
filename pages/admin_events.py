import streamlit as st # type: ignore
from streamlit_calendar import calendar # type: ignore
from datetime import datetime

from connect import get_upcoming_loc_labs_db

from navigation import generate_sidebar

st.set_page_config(
  page_title="Manage Events",
  layout="wide"
)

try:
  if "roles" not in st.session_state or st.session_state.roles[0] != "admin":
    st.switch_page("login.py")
except:
  st.switch_page("login.py")

generate_sidebar()

st.title("Manage Events")

cal_tab, add_tab, delete_tab = st.tabs(["Calendar", "Add Event", "Delete Event"])

events_workbook = get_upcoming_loc_labs_db()
events_sheet = events_workbook.get_all_records()
events_dict = {row["School"]: (row["Time Start"], row["Time End"], row["Location"], row["Teacher"]) for row in events_sheet}

calendar_options = {
  "headerToolbar": {
    "left": "today",
    "center": "title",
    "right": "prev,next"
  },
  "initialView": "dayGridMonth",
}

calendar_events = []
for event in events_sheet:
  iso_start_time = datetime.strptime(f"{event["Date"]} {event["Time Start"]}", "%m/%d/%Y %I:%M %p").isoformat()
  iso_end_time = datetime.strptime(f"{event["Date"]} {event["Time End"]}", "%m/%d/%Y %I:%M %p").isoformat()

  calendar_events.append({
    "title": f"LOC Lab @ {event["School"]}",
    "start": iso_start_time,
    "end": iso_end_time,
  })

with cal_tab:
  calendar_container = st.container(border=True)

  with calendar_container:
    view = st.selectbox("**Calendar View**", ["Month", "Time Grid"])

    if view == "Month":
      calendar_options["initialView"] = "dayGridMonth"
    else:
      calendar_options["initialView"] = "timeGridWeek"

    st.divider()
    lab_calendar = calendar(events=calendar_events, options=calendar_options)

with add_tab:
  form_container = st.container(border=True)
  with form_container:
    start_time = st.time_input(label="**Start Time**", value=None, step=300)
    if start_time: st.write(f"*Selected Time in 12-hour format: {start_time.strftime("%I:%M %p")}*")

    end_time = st.time_input(label="**End Time**", value=None, step=300)
    if end_time: st.write(f"*Selected Time in 12-hour format: {end_time.strftime("%I:%M %p")}*")

    date = st.date_input("**Date**", value=None, format="MM/DD/YYYY")
    if date:
      date_phrase = date.strftime("%A, %B %d, %Y")
      st.write(f"*Selected Date in Text: {date_phrase}*")

    with st.form("add_event_mini_form", clear_on_submit=True, border=False):
      school = st.text_input("**School**", value=None, placeholder="School", max_chars=20)

      location = st.text_input("**Location in School**", value=None, placeholder="Location", max_chars=20)

      teacher_name = st.text_input("**Teacher's/Admin's Name**", value=None, placeholder="First Name Last Name", max_chars=50)

      submitted = st.form_submit_button()

    inputs = (start_time, end_time, date, school, location)

    with st.empty():
      if submitted and None not in inputs:
        st.success("Form Submitted!")

        add_event_inputs = {
          "Start Time": start_time,
          "End Time": end_time,
          "Date": date,
          "School": school,
          "Location": location
        }

        new_row = [date.strftime("%m/%d/%Y"), school, start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p"), location, teacher_name]
        events_workbook.append_row(new_row)

      elif submitted and None in inputs:
        st.error("All fields must be filled!")

with delete_tab:
  delete_container = st.container(border=True)
  with delete_container:
    calendar_events