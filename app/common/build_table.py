from snowflake.snowpark.session import Session

def build_cost_centre_table(session: Session) -> None:
    sql = """
        insert into policies.login_navn_kostnadssted (login_navn, kostnadssted, _opprettet_dato) (
        with tilstand_n as ( 
            select *, 
                row_number() over (
                    partition by login_navn, kostnadssted 
                    order by _opprettet_dato desc, _slettet_dato desc nulls first 
                ) as n 
            from policies.login_navn_kostnadssted
        ) 
        select login_navn, kostnadssted, current_date from policies.tilganger 
        where not exists (
            select 1 
            from tilstand_n 
            where n=1 
                and _slettet_dato is null 
                and tilstand_n.login_navn = tilganger.login_navn 
                and tilstand_n.kostnadssted = tilganger.kostnadssted
        ))
    """
    session.sql(sql).collect()
    sql = """
        update policies.login_navn_kostnadssted set _slettet_dato = current_date 
        where not exists (
            select 1 
            from policies.tilganger 
            where login_navn_kostnadssted.login_navn = tilganger.login_navn 
                and login_navn_kostnadssted.kostnadssted = tilganger.kostnadssted
        ) and _slettet_dato is null
    """
    session.sql(sql).collect()

def build_task_table(session: Session) -> None:
    sql = """
        create or replace table policies.login_navn_oppgave as
        select distinct
            users.login_name as login_navn, 
            relasjon.oppgave
        from grupper
        join gruppe_oppgave_relasjoner relasjon on grupper.gruppe = relasjon.gruppe
        join gruppemedlemskap medlem on grupper.gruppe = medlem.gruppe
        join users on lower(users.email) = lower(medlem.epost)
    """
    #session.sql(sql).collect()

