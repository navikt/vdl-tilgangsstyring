import streamlit as st
from snowflake.snowpark.context import get_active_session

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

st.title("Grupper")
left, right = st.columns([0.6, 0.4]) # lage venstre side litt bredere enn høyre side


right.markdown( " ### Legg til en ny gruppe")
with right.form("Legg til gruppe"):

    group = st.text_input('Gruppenavn:')
    group_desc = st.text_input('Gruppebeskrivelse:')
    submit_group = st.form_submit_button('Lag ny gruppe')

if submit_group:
        exists_statement = f"""
            SELECT * FROM grupper WHERE gruppe = upper('{group}') and _slettet_dato is null
        """
        df_exists = session.sql(exists_statement).to_pandas()
        if df_exists.empty:
            insert_statment=f"""
                INSERT INTO grupper (
                    gruppe,
                    gruppe_beskrivelse,
                    _opprettet_av,
                    _opprettet_dato, 
                    _oppdatert_av,
                    _oppdatert_dato
                ) 
                VALUES (
                    upper('{group}'),
                    '{group_desc}',
                    '{st.experimental_user["email"]}',
                    current_date, 
                    '{st.experimental_user["email"]}',
                    current_date 
                )"""
            session.sql(insert_statment).collect()
            right.success('Suksess!', icon="✅") 
        else:
            right.error('Gruppen eksistrer allerede', icon="🚨")


right.markdown( " ### Slett en gruppe")
with right.form("Slett gruppe"):
    available_groups_statement = f"""
            SELECT gruppe FROM grupper WHERE _slettet_dato is null
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    available_groups = [row[0] for row in df_available_groups]
    group = st.selectbox("Velg gruppe",df_available_groups)
    delete_group = st.form_submit_button('Slett grupppe')

if delete_group:
    delete_statment=f"""
        update grupper set 
            _oppdatert_av = '{st.experimental_user["email"]}',
            _oppdatert_dato = current_date, 
            _slettet_dato = current_date
        where gruppe = upper('{group}')
        """
    session.sql(delete_statment).collect()
    right.success('Suksess!', icon="✅")  

left.markdown( " ### Oversikt over grupper")

gruppe_view = f"""SELECT gruppe, gruppe_beskrivelse FROM grupper WHERE _slettet_dato IS NULL"""
df_groups = session.sql(gruppe_view).to_pandas()
left.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)


