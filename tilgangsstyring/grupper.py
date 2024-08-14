import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# Get the current credentials
session = get_active_session()

st.title("Grupper")

query= "SELECT gruppe, gruppe_beskrivelse FROM grupper WHERE _slettet_dato IS NULL"
df = session.sql(query)
queried_data = df.to_pandas()
st.table(data=queried_data)
#queried_data = df.to_pandas()
#st.dataframe(pd.DataFrame(df, columns=["Gruppe", "Gruppebeskrivelse"]), hide_index=True)


if st.button("+ Lag ny gruppe"):

    
    st.title("Lag ny gruppe")
    gruppenavn = st.text_input("Gruppenavn")
    gruppe_beskrivelse = st.text_input("Gruppebeskrivelse")

    if st.button("Send inn"):
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
        session.sql(query)

        # TODO: refresh knapp?


