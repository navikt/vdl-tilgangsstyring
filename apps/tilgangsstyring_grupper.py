import os
import streamlit as st
import snowflake.connector
from snowflake.connector.errors import ProgrammingError
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_snowflake_connection():
    if "snowflake_conn" not in st.session_state:
        st.session_state.snowflake_conn = snowflake.connector.connect(
            **snowflake_config
        )
    return st.session_state.snowflake_conn

def get_current_user(conn):
    if "current_user" not in st.session_state:
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_USER()")
        st.session_state.current_user = cursor.fetchone()[0]
        cursor.close()
    return st.session_state.current_user

def check_user_role(conn, required_role):
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_ROLE()")
    current_role = cursor.fetchone()[0].lower()
    cursor.close()
    return current_role == required_role

def execute_query(conn, query, params=None):
    try:
        with conn.cursor() as cur:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if query.strip().upper().startswith('SELECT'):
                return cur.fetchall(), True
            else:
                conn.commit()
                return None, True
    except ProgrammingError as e:
        st.error(f"Error executing query: {e}")
        return None, False

def get_group_names(conn):
    query = "SELECT gruppe FROM grupper WHERE _slettet_dato IS NULL"
    results, _ = execute_query(conn, query)
    return [row[0] for row in results] if results else []

# Add group form
def add_group_form(conn):
    with st.form("new_group_form"):
        gruppenavn = st.text_input("Gruppenavn")
        gruppe_beskrivelse = st.text_input("Gruppebeskrivelse")

        if st.form_submit_button("Send inn"):
                st.session_state
                query = f"""
                    MERGE INTO grupper old USING (
                        SELECT 
                            '{gruppenavn}' as gruppe,
                            '{gruppe_beskrivelse}' as gruppe_beskrivelse,
                            current_user as _opprettet_av,
                            current_date as _opprettet_dato, 
                            current_user as _oppdatert_av,
                            current_date as _oppdatert_dato 
                        ) new_row ON new_row.gruppe = old.gruppe
                    WHEN MATCHED AND old._slettet_dato IS NULL THEN UPDATE SET 
                        old.gruppe_beskrivelse = new_row.gruppe_beskrivelse, 
                        old._oppdatert_av = new_row._oppdatert_av,
                        old._oppdatert_dato = new_row._oppdatert_dato 
                    WHEN NOT MATCHED THEN INSERT (
                        old.gruppe, 
                        old.gruppe_beskrivelse,
                        old._opprettet_av,
                        old._opprettet_dato, 
                        old._oppdatert_av,
                        old._oppdatert_dato
                    ) VALUES (
                        new_row.gruppe, 
                        new_row.gruppe_beskrivelse,
                        new_row._opprettet_av,
                        new_row._opprettet_dato, 
                        new_row._oppdatert_av,
                        new_row._oppdatert_dato
                    )
                """
                try:
                    with conn.cursor() as cur:
                        cur.execute(query)
                    st.success("Suksess: gruppe laget")
                    st.session_state.page = "home"
                    st.experimental_rerun()  # Return to home page after submission

                except ProgrammingError as e:
                    st.error(f"Error executing query: {e}")


# Delete group form
def delete_group_form(conn, group_names):
    with st.form("delete_group_form"):
        group_to_delete = st.selectbox("Velg gruppe å slette", group_names)

        if st.form_submit_button("Bekreft sletting"):
            query = "UPDATE grupper SET _slettet_dato = %s WHERE gruppe = %s"
            _, success = execute_query(conn, query, (datetime.now(), group_to_delete))
            if success:
                st.success("Suksess: gruppe slettet")
                st.session_state.page = "home"
                st.experimental_rerun()  # Return to home page after submission
        if st.form_submit_button("Tilbake til forside"):
            st.session_state.page = "home"
            st.experimental_rerun()  # Return to home page

# Group details page
def group_details_page(conn):
    st.title(f"Gruppedetaljer: {st.session_state.selected_group}")

    # Display users in the group
    query = """
    SELECT epost, fra_dato, til_dato
    FROM gruppemedlemskap
    WHERE gruppe = %s
    """
    results, _ = execute_query(conn, query, (st.session_state.selected_group,))
    if results:
        df = pd.DataFrame(results, columns=["E-post", "Fra dato", "Til dato"])
        st.dataframe(df)
    else:
        st.write("Ingen medlemmer i gruppen")

    # Add new user to group
    if st.button("+ Legg til nytt medlem"):
        with st.form("new_user_form"):
            email = st.text_input("E-post")
            from_date = st.date_input("Fra dato")
            to_date = st.date_input("Til dato")
            if st.form_submit_button("Send inn"):
                query = """
                INSERT INTO gruppemedlemskap (epost, gruppe, fra_dato, til_dato, _opprettet_av, _opprettet_dato, _slettet_dato)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                _, success = execute_query(conn, query, (email, st.session_state.selected_group, from_date, to_date, st.session_state.current_user, datetime.now(), None)) 
                if success:
                    st.success("Suksess: medlem lagt til")
                    st.experimental_rerun()  # Refresh the page to show the updated group
                else:
                    st.error("Error: klarte ikke legge til medlem, se logger for mer info.")

    if st.button("Tilbake til forside"):
        st.session_state.page = "home"
        st.experimental_rerun()  # Return to home page

# Home page
def home_page(conn):
    st.title("Tilgangsstyring")

    # Dropdown to select group
    #group_names = get_group_names(conn)
    #selected_group = st.selectbox("Velg gruppe", group_names)

    query= "SELECT gruppe, gruppe_beskrivelse FROM grupper WHERE _slettet_dato IS NULL"
    with conn.cursor() as cursor: 
        cursor.execute(query)
        logs = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        st.dataframe(pd.DataFrame(logs, columns=columns), hide_index=True)
    
    # Buttons for group actions
    #if st.button("Se gruppedetaljer"):
    #    st.session_state.page = "group_details"
    #    st.session_state.selected_group = selected_group
    #    st.experimental_rerun()

    if st.button("+ Legg til gruppe"):
        st.session_state.page = "add_group"

    #if st.button("Slett gruppe"):
    #    st.session_state.page = "delete_group"

    # Handle different pages based on selected action
    if st.session_state.page == "add_group":
        add_group_form(conn)
    #elif st.session_state.page == "delete_group":
    #    delete_group_form(conn, group_names)

# Main app logic
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Attempt to connect to Snowflake
    try:
        conn = get_snowflake_connection()
    except Exception as e:
        st.error("Failed to connect to Snowflake. Please make sure you're authenticated via Azure AD.")
        st.stop()
    
    # Check if user has the required role
    if not check_user_role(conn, "tilgangsstyring_transformer"):
        st.error("You do not have the necessary permissions to use this app.")
        conn.close()
        st.stop()
    st.success("Successfully authenticated with the correct role.")

    # Get the current user
    if "current_user" not in st.session_state:
        st.session_state.current_user = get_current_user(conn)

    # Page routing based on session state
    if st.session_state.page == "home":
        home_page(conn)
    elif st.session_state.page == "group_details":
        group_details_page(conn)
    elif st.session_state.page == "add_group":
        add_group_form(conn)
    elif st.session_state.page == "delete_group":
        delete_group_form(conn, get_group_names(conn))

if __name__ == "__main__":
    main()
