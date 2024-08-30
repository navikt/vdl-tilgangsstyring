import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from common.utils import check_role
# Set page layout to wide
st.set_page_config(layout="wide")

def valid_email(email) -> bool:
    # Check if the email contains one “@” symbol
    if email.count('@') != 1:
        return False

    # Split the email into local part and domain part
    local_part, domain_part = email.split('@')

    # Check if both the local part and domain part are not empty
    if len(local_part) == 0 or len(domain_part) == 0:
        return False

    # Check if the domain part contains a dot (.)
    if domain_part.find('.') == -1:
        return False

    return True

# Get the current credentials
session = get_active_session()
check_role(session)



st.title("Gruppemedlemskap")
left, right = st.columns([0.7, 0.3])


right.markdown( " ### Legg til et nytt medlem")


with right.form("Legg til medlem"):
    available_groups_statement = f"""
            SELECT gruppe FROM grupper WHERE _slettet_dato is null
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_available_groups)
    available_users_statement = f"""
            SELECT email FROM users 
        """
    df_available_users = session.sql(available_users_statement).to_pandas()
    email = st.selectbox("E-post",df_available_users) # TODO: bytte til multiselect?
    from_date_input = st.date_input("Fra dato")
    to_date_input = st.date_input("Til dato")
    submit_group = st.form_submit_button('Legg til gruppemedlemskap')
    
if submit_group:
    from_date = f"{from_date_input.day}-{from_date_input.month}-{from_date_input.year}"
    to_date = f"{to_date_input.day}-{to_date_input.month}-{to_date_input.year}"
    exists_statement = f"""
        SELECT * 
        FROM gruppemedlemskap
        WHERE gruppe = upper('{group}') 
          AND epost = initcap('{email}') 
          AND _slettet_dato is null 
          AND current_date between fra_dato and til_dato
    """
    df_exists = session.sql(exists_statement).to_pandas()
    if df_exists.empty:
        if valid_email(email):
            insert_statment=f"""
                INSERT INTO gruppemedlemskap (
                    gruppe,
                    epost,
                    fra_dato, 
                    til_dato,
                    _opprettet_av,
                    _opprettet_dato, 
                    _oppdatert_av,
                    _oppdatert_dato
                ) VALUES (
                    upper('{group}'),
                    initcap('{email}') ,
                    to_date('{from_date}','DD-MM-YYYY'),
                    to_date('{to_date}','DD-MM-YYYY'),
                    '{st.experimental_user["email"]}',
                    current_date, 
                    '{st.experimental_user["email"]}',
                    current_date 
                )
            """
            session.sql(insert_statment).collect()
            right.success('Suksess!', icon="✅")    
        else:
            right.error("Ikke kødd, skriv inn en ordentlig e-post adresse", icon="🚨")
    else:
        right.error('Dette medlemmet finnes allerede i gruppen', icon="🚨")



right.markdown( " ### Slett medlem fra gruppe")
with right.form("Slett Gruppe"):

    available_groups_statement = f"""
            SELECT distinct gruppe 
            FROM gruppemedlemskap 
            WHERE _slettet_dato is null 
              AND current_date <= til_dato
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_available_groups)

    available_emails_statement = f"""
            SELECT epost 
            FROM gruppemedlemskap
            WHERE _slettet_dato is null 
              AND gruppe = upper('{group}')
              AND current_date <= til_dato
        """
    df_available_emails = session.sql(available_emails_statement).to_pandas()
    email = st.selectbox("Velg e-post", df_available_emails)
    delete_group = st.form_submit_button('Slett gruppemedlemskap')

if delete_group:
    delete_statment=f"""
        update gruppemedlemskap set 
            _oppdatert_av = '{st.experimental_user["email"]}',
            _oppdatert_dato = current_date, 
            _slettet_dato = current_date
        where gruppe = upper('{group}')
        and epost = initcap('{email}')
        """
    session.sql(delete_statment).collect()
    right.success('Suksess!', icon="✅")  

left.markdown( " ### Oversikt over medlemmer")

gruppe_view = f"""
    SELECT gruppe
         , epost, fra_dato, til_dato 
    FROM gruppemedlemskap 
    WHERE _slettet_dato IS NULL 
    AND current_date <= til_dato
    """
df_groups = session.sql(gruppe_view).to_pandas()
left.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)