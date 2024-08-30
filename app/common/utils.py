import streamlit as st
import pandas as pd
from snowflake.snowpark.session import Session


def check_role(session: Session) -> None:
    required_roles = ("TILGANGSSTYRING_USER", "TILGANGSSTYRING_DEVELOPER")
    current_role = session.get_current_role().strip('"')
    if current_role not in required_roles:
        st.error(f"Your role {current_role} do not have the necessary permissions to use this app. Required role is TILGANGSSTYRING_USER, please switch roles.")
        st.stop()
    st.success("Successfully authenticated with the correct role.")