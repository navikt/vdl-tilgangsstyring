import streamlit as st
from snowflake.snowpark.context import get_active_session

# from common.utils import check_role

# Set page layout to wide
st.set_page_config(layout="wide", page_title="Kostnadsstedsrelasjoner")

# Get the current credentials
session = get_active_session()
required_roles = (
    "TILGANGSSTYRING_USER",
    "TILGANGSSTYRING_DEVELOPER",
    "TILGANGSSTYRING_REPORTER",
)
current_role = session.get_current_role().strip('"')
if current_role not in required_roles:
    st.error(
        f"Your role {current_role} do not have the necessary permissions to use this app. Required role is TILGANGSSTYRING_USER, please switch roles."
    )
    st.stop()
st.success("Successfully authenticated with the correct role.")


st.title("Tilganger")


st.markdown("### Gi tilgang")


with st.form("Opprett tilgang"):
    cost_centres_query = f"""
            SELECT DISTINCT gruppe FROM kostnadssted_grupper ORDER BY 1
        """
    tasks_query = f"""
            SELECT DISTINCT gruppe FROM oppgave_grupper
        """
    accounts_query = f"""
            SELECT DISTINCT gruppe FROM artskonto_grupper
        """
    email = st.experimental_user["email"]
    cost_centre = st.selectbox(
        "Angi Kostnadssted", session.sql(cost_centres_query).to_pandas()
    )
    tasks = st.selectbox("Angi Oppgave Gruppe", session.sql(tasks_query).to_pandas())
    account = st.selectbox(
        "Angi Artskonto Gruppe", session.sql(accounts_query).to_pandas()
    )
    roles = st.selectbox("Angi Rolle", ["DETALJER", "IKKE DETALJER"])
    from_date_input = st.date_input("Fra dato")
    to_date_input = st.date_input("Til dato")
    reason = st.text_input("Tilgangbegrunnelse:")
    submit = st.form_submit_button("Gi tilgang")

if submit:
    from_date = f"{from_date_input.day}-{from_date_input.month}-{from_date_input.year}"
    to_date = f"{to_date_input.day}-{to_date_input.month}-{to_date_input.year}"
    already_exists = f"""
        SELECT 
            epost,
            kostnadssted_gruppe,
            oppgave_gruppe,
            artskonto_gruppe,
            rolle
        FROM bruker_tilganger
        WHERE epost=initcap('{email}')
        AND kostnadssted_gruppe='{cost_centre}'
        AND oppgave_gruppe='{tasks}'
        AND artskonto_gruppe='{account}'
        AND _slettet_dato is null 
        AND current_date <= til_dato
    """
    if session.sql(already_exists).to_pandas().empty:
        insert_statment = f""" 
            INSERT INTO bruker_tilganger (
                epost,
                kostnadssted_gruppe,
                oppgave_gruppe,
                artskonto_gruppe,
                rolle,
                begrunnelse, 
                fra_dato,
                til_dato,
                tilgang_gitt_av,
                tilgang_gitt_fra
            ) VALUES (
                initcap('{email}'),
                '{cost_centre}',
                '{tasks}',
                '{account}',
                '{roles}',
                '{reason}',
                to_date('{from_date}','DD-MM-YYYY'),
                to_date('{to_date}','DD-MM-YYYY'),
                '{st.experimental_user["email"]}',
                current_timestamp
            )
        """
        session.sql(insert_statment).collect()
        st.success("Suksess!", icon="✅")
    else:
        st.error("Tilgangen existerer eksisterer allerede", icon="🚨")

st.markdown(" ### Søk opp bruker")
with st.form("Søk opp bruker"):
    show_submit = st.form_submit_button("Vis tilganger")
if show_submit:
    query = f"""
        SELECT * 
        FROM bruker_tilganger 
        WHERE epost = initcap('{st.experimental_user["email"]}')
        AND _slettet_dato is null 
        AND current_date <= til_dato
    """
    df = session.sql(query).to_pandas()
    st.dataframe(df, on_select="rerun", hide_index=True, use_container_width=True)

st.markdown(" ### Slett en kostnadsstedsrelasjon")
with st.form("Slett tilgang"):
    cost_centre_query = f"""
        SELECT DISTINCT
            kostnadssted_gruppe
        FROM bruker_tilganger
        WHERE _slettet_dato is null 
        AND epost = initcap('{st.experimental_user["email"]}')
        AND current_date <= til_dato
        """
    tasks_query = f"""
        SELECT DISTINCT
            oppgave_gruppe
        FROM bruker_tilganger
        WHERE _slettet_dato is null 
        AND epost = initcap('{st.experimental_user["email"]}')
        AND current_date <= til_dato
        """
    account_query = f"""
        SELECT DISTINCT
            artskonto_gruppe
        FROM bruker_tilganger
        WHERE _slettet_dato is null 
        AND epost = initcap('{st.experimental_user["email"]}')
        AND current_date <= til_dato
        """
    email = st.experimental_user["email"]
    cost_centre = st.selectbox(
        "Angi Kostnadssted", session.sql(cost_centre_query).to_pandas()
    )
    tasks = st.selectbox("Angi Oppgave Gruppe", session.sql(tasks_query).to_pandas())
    account = st.selectbox(
        "Angi Artskonto Gruppe", session.sql(account_query).to_pandas()
    )
    delete_submit = st.form_submit_button("Slett bruker tilgang")
if delete_submit:
    already_exists = f"""
        SELECT 
            epost,
            kostnadssted_gruppe,
            oppgave_gruppe,
            artskonto_gruppe,
            rolle
        FROM bruker_tilganger
        WHERE epost=initcap('{email}')
        AND kostnadssted_gruppe='{cost_centre}'
        AND oppgave_gruppe='{tasks}'
        AND artskonto_gruppe='{account}'
        AND _slettet_dato is null 
        AND current_date <= til_dato
    """
    if not session.sql(already_exists).to_pandas().empty:
        update_statment = f""" 
            UPDATE bruker_tilganger SET _slettet_dato = current_date()
            WHERE 1=1
                AND epost = initcap('{email}')
                AND kostnadssted_gruppe = '{cost_centre}'
                AND oppgave_gruppe = '{tasks}'
                AND artskonto_gruppe = '{account}'
                AND _slettet_dato is null 
                AND current_date <= til_dato
        """
        session.sql(update_statment).collect()
        st.success("Suksess!", icon="✅")
    else:
        st.error("Tilgangen eksisterer ikke", icon="🚨")

with st.form("Oppdater tilganger"):
    update_access = st.form_submit_button("Oppdater brukertilgang")
if update_access:
    try:
        query = f"""
            insert into tilgangsstyring.policies.bruker_tilganger 
            select * from tilgangsstyring.policies.beregnet_bruker_tilganger src 
            where not exists (
            select 1 from tilgangsstyring.policies.bruker_tilganger trgt 
            where src.login_navn=trgt.login_navn 
            and src.kostnadssted_gruppe=trgt.kostnadssted_gruppe
            and src.kostnadssted=trgt.kostnadssted
            and src.oppgave_gruppe=trgt.oppgave_gruppe
            and coalesce(src.oppgave,'¿nothing¿')=coalesce(trgt.oppgave,'¿nothing¿')
            and src.artskonto_gruppe=trgt.artskonto_gruppe
            and coalesce(src.artskonto,'¿nothing¿')=coalesce(trgt.artskonto,'¿nothing¿')
            and src.rolle=trgt.rolle
            )
            """
        session.sql(query).collect()
        st.success("Suksess!", icon="✅")
    except:
        st.error("Failed", icon="🚨")

    try:
        query = f"""
            delete from tilgangsstyring.policies.bruker_tilganger trgt
            where not exists (
            select 1 from tilgangsstyring.policies.beregnet_bruker_tilganger src
            where src.login_navn=trgt.login_navn 
            and src.kostnadssted_gruppe=trgt.kostnadssted_gruppe
            and src.kostnadssted=trgt.kostnadssted
            and src.oppgave_gruppe=trgt.oppgave_gruppe
            and coalesce(src.oppgave,'¿nothing¿')=coalesce(trgt.oppgave,'¿nothing¿')
            and src.artskonto_gruppe=trgt.artskonto_gruppe
            and coalesce(src.artskonto,'¿nothing¿')=coalesce(trgt.artskonto,'¿nothing¿')
            and src.rolle=trgt.rolle
            )
            """
        session.sql(query).collect()
        st.success("Suksess!", icon="✅")
    except:
        st.error("Failed", icon="🚨")
