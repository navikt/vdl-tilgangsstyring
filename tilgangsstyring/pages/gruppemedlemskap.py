import streamlit as st
import pandas as pd
from snowflake.connector.errors import ProgrammingError
from snowflake.snowpark.context import get_active_session

# Get the current credentials
session = get_active_session()

st.title("Gruppemedlemskap")
gruppe_view = f"""SELECT gruppe, epost FROM gruppemedlemskap WHERE _slettet_dato IS NULL and current_date between fra_dato and til_dato"""
df_groups = session.sql(gruppe_view).to_pandas()
st.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)

with st.form("Legg til medlem"):
    available_groups_statement = f"""
            SELECT gruppe FROM grupper WHERE _slettet_dato is null
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    available_groups = [row[0] for row in df_available_groups]
    group = st.selectbox("ledig grupper",df_available_groups)
    email = st.text_input("E-post")
    from_date = st.date_input("Fra dato")
    to_date = st.date_input("Til dato")
    submit_group = st.form_submit_button('Legg til')

if submit_group:
        st.success(st.markdown(from_date.isoformat))
        #exists_statement = f"""
        #    SELECT * 
        #    FROM gruppemedlemskap
        #    WHERE gruppe = upper('{group}') 
        #      AND epost = lower('{email}') 
        #      AND _slettet_dato is null 
        #      AND current_date between fra_dato and til_dato
        #"""
        #df_exists = session.sql(exists_statement).to_pandas()
        #if df_exists.empty:
        #    insert_statment=f"""
        #        INSERT INTO gruppemedlemskap (
        #            gruppe,
        #            epost,
        #            fra_dato, 
        #            til_dato,
        #            _opprettet_av,
        #            _opprettet_dato, 
        #            _oppdatert_av,
        #            _oppdatert_dato
        #        ) 
        #        VALUES (
        #            upper('{group}'),
        #            lower('{email}') ,
        #            {from_date},
        #            {to_date},
        #            '{st.experimental_user["email"]}',
        #            current_date, 
        #            '{st.experimental_user["email"]}',
        #            current_date 
        #        )"""
        #    session.sql(insert_statment).collect()
        #    st.success('Success!', icon="✅")    
        #else:
        #    st.success('Already exists')
        #st.rerun()

with st.form("Slett Gruppe"):
    available_groups_statement = f"""
            SELECT gruppe 
            FROM gruppemedlemskap 
            WHERE _slettet_dato is null 
              AND current_date between fra_dato and til_dato
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    available_groups = [row[0] for row in df_available_groups]    
    group = st.selectbox("ledig grupper",df_available_groups)
    available_emails_statement = f"""
            SELECT epost 
            FROM gruppemedlemskap
            WHERE _slettet_dato is null 
              AND gruppe = '{group}'
              AND current_date between fra_dato and til_dato
        """
    df_available_emails = session.sql(available_emails_statement).to_pandas()
    available_emails = [row[0] for row in df_available_emails]    
    email = st.selectbox("ledig eposter",df_available_emails)
    delete_group = st.form_submit_button('Slett gruppemedlemskap')

if delete_group:
    delete_statment=f"""
        update gruppemedlemskap set 
            _oppdatert_av = '{st.experimental_user["email"]}',
            _oppdatert_dato = current_date, 
            _slettet_dato = current_date
        where gruppe = upper('{group}')
        and epost = lower('{email}')
        """
    session.sql(delete_statment).collect()
    st.success('Success!', icon="✅")  
    st.rerun()

