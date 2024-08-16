import streamlit as st
import pandas as pd
from snowflake.connector.errors import ProgrammingError
from snowflake.snowpark.context import get_active_session

# Get the current credentials
session = get_active_session()

st.title("Grupper")
left, right = st.columns(2)


right.write(
    """
    Legge til en ny gruppe
    """
)
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
            right.success('Success!', icon="✅")
        else:
            right.error('Already exists', icon="🚨")


right.write(
    """
    Slette gruppe
    """
)
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
    right.success('Success!', icon="✅")  

left.write(
    """
    Tekst her.
    """
)

gruppe_view = f"""SELECT gruppe, gruppe_beskrivelse FROM grupper WHERE _slettet_dato IS NULL"""
df_groups = session.sql(gruppe_view).to_pandas()
left.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)

