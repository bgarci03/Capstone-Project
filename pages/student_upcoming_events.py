import streamlit as st # type: ignore
from streamlit_calendar import calendar # type: ignore
from datetime import datetime

from navigation import generate_sidebar

from connect import get_upcoming_loc_labs_db

st.set_page_config(
  page_title="Upcoming Events",
  page_icon=":material/event:",
  layout="wide"
)

try:
  if "roles" not in st.session_state or st.session_state.roles[0] != "student":
    st.switch_page("login.py")
except:
  st.switch_page("login.py")

def show_event(event_info):
  st.write(event_info)

generate_sidebar()

events_sheet = get_upcoming_loc_labs_db().get_all_records()
events_filtered_dict = {row["School"]: (row["Time Start"], row["Time End"], row["Location"], row["Teacher"]) for row in events_sheet if row["School"] == st.session_state.school}

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
    "title": f"LOC Lab @ {st.session_state.school}",
    "start": iso_start_time,
    "end": iso_end_time,
  })

st.title("Upcoming Events", anchor=False)

calendar_container = st.container(border=True)

with calendar_container:
  view = st.selectbox("**Calendar View**", ["Month", "Time Grid"])

  if view == "Month":
    calendar_options["initialView"] = "dayGridMonth"
  else:
    calendar_options["initialView"] = "timeGridWeek"

  st.divider()
  lab_calendar = calendar(events=calendar_events, options=calendar_options)
