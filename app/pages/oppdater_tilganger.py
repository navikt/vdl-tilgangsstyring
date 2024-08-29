import streamlit as st
from snowflake.snowpark.context import get_active_session
from common.build_table import build_cost_centre_table, build_task_table

# Set page layout to wide
st.set_page_config(layout="wide")

# Get the current credentials
session = get_active_session()

# Check if user has the required role
required_roles = ("TILGANGSSTYRING_ADMIN", "TILGANGSSTYRING_DEVELOPER")
current_role = session.get_current_role().strip('"')
if current_role not in required_roles:
    st.error(f"Your role {current_role} do not have the necessary permissions to use this app. Required role is TILGANGSSTYRING_ADMIN, please switch roles.")
    st.stop()
st.success("Successfully authenticated with the correct role.")


st.title("Oppdater tilgangsstyring")

update_data = st.button("Oppdater")

if update_data:
    try:
        build_cost_centre_table(session=session)
        build_task_table(session=session)
        st.success('Suksess!', icon="✅") 
    except Exception as e:
        st.error(e, icon="🚨")


