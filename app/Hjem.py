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

#st.markdown("### Last opp fil")
#st.text("Her kan du laste opp en fil med eksisterende tilganger.")
#uploaded_file = st.file_uploader("Last opp fil")

sql = """
create or replace view gyldig_kostnadssted_liste as 
select distinct  
      flex_value as kostnadssted
    , description as kostnadssted_navn 
from tlost__oebs_prod.apps.xxrtv_gl_segment_v 
where flex_value_set_name = 'OR_KSTED'
order by 1;
"""
session.sql(sql).collect()
sql = """
create or replace view gyldige_oppgave_liste as
select distinct
      flex_value as oppgave
    , description as oppgave_navn 
from tlost__oebs_prod.apps.xxrtv_gl_segment_v 
where flex_value_set_name = 'OR_AKTIVITET' 
and coalesce(end_date_active,to_timestamp('9999','yyyy')) >= to_timestamp('2023','yyyy')
and enabled_flag = 'Y'
order by 1
"""
session.sql(sql).collect()