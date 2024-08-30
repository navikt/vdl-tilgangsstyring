import streamlit as st
from snowflake.snowpark.context import get_active_session

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Hjem")

# Get the current credentials
session = get_active_session()

# Check if user has the required role
required_roles = ("TILGANGSSTYRING_ADMIN", "TILGANGSSTYRING_DEVELOPER")
current_role = session.get_current_role().strip('"')
if current_role not in required_roles:
    st.error(f"Your role {current_role} do not have the necessary permissions to use this app. Required role is TILGANGSSTYRING_ADMIN, please switch roles.")
    st.stop()
st.success("Successfully authenticated with the correct role.")


st.title("Velkommen til Tilgangsstyring!")
st.markdown("Denne Streamlit appen gjør det mulig å enkelt opprette grupper som skal ha tilgang til ulike kostnadssteder og oppgaver i MicroStrategy. ")


#st.markdown("### Last opp fil")
#st.text("Her kan du laste opp en fil med eksisterende tilganger.")
#uploaded_file = st.file_uploader("Last opp fil")