import streamlit as st
from snowflake.snowpark.context import get_active_session
from common.build_table import build_cost_centre_table, build_task_table

# Set page layout to wide
st.set_page_config(layout="wide")

# Get the current credentials
session = get_active_session()

st.title("Oppdater tilgangsstyring")

update_data = st.button("Oppdater")

if update_data:
    try:
        build_cost_centre_table(session=session)
        build_task_table(session=session)
        st.success('Suksess!', icon="✅") 
    except Exception as e:
        st.error(e, icon="🚨")


