import streamlit as st
from snowflake.snowpark.context import get_active_session

# Set page layout to wide
st.set_page_config(layout="wide")

# Get the current credentials
session = get_active_session()

# Check if user has the required role
required_role = "TILGANGSSTYRING_ADMIN"
current_role = session.get_current_role().strip('"')
if current_role != required_role:
    st.error(f"Your role {current_role} do not have the necessary permissions to use this app. Required role is {required_role}, please switch roles.")
    st.stop()
st.success("Successfully authenticated with the correct role.")

st.title("Oppgaverelasjoner")

left, right = st.columns([0.7, 0.3])


right.write(
    """
    Legg til en oppgaverelasjon
    """
)


with right.form("Legg til oppgaverelasjon"):
    available_groups_statement = f"""
            SELECT gruppe FROM grupper WHERE _slettet_dato is null
        """
    df_available_groups = session.sql(available_groups_statement).to_pandas()
    available_tasks_statement = f"""
            SELECT oppgave FROM gyldige_oppgave_liste ORDER BY 1
        """
    df_available_tasks = session.sql(available_tasks_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_available_groups)
    task = st.selectbox("Velg oppgave",df_available_tasks)
    submit_group = st.form_submit_button('Legg til oppgaverelasjon')
    
if submit_group:
    exists_statement = f"""
        SELECT * 
        FROM gruppe_oppgave_relasjoner 
        WHERE gruppe = upper('{group}') 
          AND oppgave = '{task}' 
          AND _slettet_dato is null 
    """
    df_exists = session.sql(exists_statement).to_pandas()
    if df_exists.empty:
        insert_statment=f"""
            INSERT INTO gruppe_oppgave_relasjoner (
                gruppe,
                oppgave,
                _opprettet_av,
                _opprettet_dato, 
                _oppdatert_av,
                _oppdatert_dato
            ) VALUES (
                upper('{group}'),
                '{task}',
                '{st.experimental_user["email"]}',
                current_date, 
                '{st.experimental_user["email"]}',
                current_date 
            )
        """
        session.sql(insert_statment).collect()
        right.success('Suksess!', icon="✅") 
    else:
        right.error('Oppgaverelasjon eksisterer allerede', icon="🚨")

right.write(
    """
    Slett en oppgaverelasjon
    """
)
with right.form("Slett Gruppe"):
    groups_for_delete_statement = f"""
            SELECT distinct gruppe 
            FROM gruppe_oppgave_relasjoner 
            WHERE _slettet_dato is null 
            ORDER BY 1
        """
    df_groups_for_delete = session.sql(groups_for_delete_statement).to_pandas()
    group = st.selectbox("Velg gruppe",df_groups_for_delete)
    task_for_delete_statement = f"""
            SELECT oppgave 
            FROM gruppe_oppgave_relasjoner
            WHERE _slettet_dato is null 
              AND gruppe = '{group}'
            ORDER BY 1
        """
    df_task_for_delete = session.sql(task_for_delete_statement).to_pandas()
    task = st.selectbox("Velg oppgave",df_task_for_delete)
    delete_group = st.form_submit_button('Slett oppgaverelasjon')

if delete_group:
    delete_statment=f"""
        update gruppe_oppgave_relasjoner set 
            _oppdatert_av = '{st.experimental_user["email"]}',
            _oppdatert_dato = current_date, 
            _slettet_dato = current_date
        where gruppe = upper('{group}')
        and oppgave = '{task}'
        """
    session.sql(delete_statment).collect()
    right.success('Suksess!', icon="✅")  
    # st.rerun()

left.write(
    """
    Oversikt over alle oppgaverelasjoner
    """
)
gruppe_view = f"""
    SELECT 
        grp.gruppe, 
        grp.oppgave,
        oppg.oppgave_navn
    FROM gruppe_oppgave_relasjoner grp 
    JOIN gyldige_oppgave_liste oppg on oppg.oppgave = grp.oppgave 
    WHERE _slettet_dato IS NULL 
    """
df_groups = session.sql(gruppe_view).to_pandas()
left.dataframe(df_groups, on_select="rerun", hide_index=True, use_container_width=True)