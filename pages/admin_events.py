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

get_upcoming_loc_labs_db()
events_workbook = st.session_state.upcoming_loc_sheet
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

        new_row = [date.strftime("%m/%d/%Y"), school, start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p"), location, teacher_name]
        events_workbook.append_row(new_row)

      elif submitted and None in inputs:
        st.error("All fields must be filled!")

with delete_tab:
  delete_container = st.container(border=True)
  with delete_container:
    school_name = st.text_input("**School Name**", value=None, max_chars=20)

    school_events = [row for row in events_sheet if row["School"] == school_name]

    try:
      event_date = st.date_input("**Event Date**", value=None, format="MM/DD/YYYY")

      school_events_with_date = [row for row in school_events if row["Date"] == event_date.strftime("%m/%d/%Y")]

      if school_events_with_date:
        st.dataframe(school_events_with_date, use_container_width=True)
      else:
        st.error("No events found with the selected high school and date!")
    except AttributeError:
      st.error("Enter a date!")
    except:
      st.error("An unkown error occured! Please refresh the page or contact IT!")
    else:
      start_time = st.time_input(label="**Event Start Time**", value=None, step=300)
      if start_time: st.write(f"*Selected Time in 12-hour format: {start_time.strftime("%I:%M %p")}*")

      end_time = st.time_input(label="**Event End Time**", value=None, step=300)
      if end_time: st.write(f"*Selected Time in 12-hour format: {end_time.strftime("%I:%M %p")}*")

      location = st.text_input("**Location in School**", value=None, max_chars=20)

      teacher_name = st.text_input("**Teacher's/Admin's Name**", value=None, max_chars=50)

      try:
        inputs = (event_date.strftime("%m/%d/%Y"), school_name, start_time.strftime("%I:%M %p"), end_time.strftime("%I:%M %p"), location, teacher_name)
      except AttributeError:
        inputs = (None,)

      for i, event in enumerate(events_sheet):
        found_match = tuple(event.values()) == inputs

        if found_match:
          st.write("**Event to be deleted!**")
          st.dataframe(event, use_container_width=True)
          break

      with st.form("delete_event_mini_form", clear_on_submit=True, border=False):
        submitted = st.form_submit_button()
      
      if found_match and submitted and None not in inputs:
        events_workbook.delete_rows(i + 2)
        st.success("Event Deleted!")

        st.rerun()
        
      elif submitted and None in inputs:
        st.error("All fields must be filled!")
      
      elif not found_match and submitted:
        st.error("No event found!")
