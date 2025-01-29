import streamlit as st # type: ignore
from st_supabase_connection import SupabaseConnection # type: ignore

conn = st.connection("supabase", type=SupabaseConnection)

# Perform query.
rows = conn.table("mytable").select("*").execute()

# Print results.
for row in rows.data:
  st.write(f"{row['name']} has a :{row['pet']}:")
