import streamlit as st
from snowflake.snowpark.context import get_active_session
from common.utils import check_role

# Set page layout to wide
st.set_page_config(page_title="Hjem", layout="wide")

# Get the current credentials
session = get_active_session()
check_role(session)


st.title("Velkommen til Tilgangsstyring!")
st.markdown("""Denne Streamlit appen gjør det mulig å enkelt opprette grupper 
            som skal ha tilgang til ulike kostnadssteder og oppgaver i MicroStrategy. """)
st.markdown("Her kan du:")
st.markdown("""
    * Lage nye tilgangsgrupper
    * Legge til medlemmer i tilgangsgrupper
    * Legge til kostnadsstedsrelasjoner i tilgangsgruppene (i.e. hvilke kostnadssteder medlemmene i gruppen skal ha tilgang til)
    * Legge til oppgaverelasjoner i tilgangsgruppene (i.e. hvilke oppgaver medlemmene i gruppen skal ha tilgang til)

""")