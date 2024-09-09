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
        select login_navn, kostnadssted, current_date from policies.tilganger_kostnadssted tilganger
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
            from policies.tilganger_kostnadssted tilganger
            where login_navn_kostnadssted.login_navn = tilganger.login_navn 
                and login_navn_kostnadssted.kostnadssted = tilganger.kostnadssted
        ) and _slettet_dato is null
    """
    session.sql(sql).collect()

def build_task_table(session: Session) -> None:

    sql = """
        insert into policies.login_navn_oppgave (login_navn, oppgave, _opprettet_dato) (
        with tilstand_n as ( 
            select *, 
                row_number() over (
                    partition by login_navn, oppgave 
                    order by _opprettet_dato desc, _slettet_dato desc nulls first 
                ) as n 
            from policies.login_navn_oppgave
        ) 
        select login_navn, oppgave, current_date from policies.tilganger_oppgave tilganger
        where not exists (
            select 1 
            from tilstand_n 
            where n=1 
                and _slettet_dato is null 
                and tilstand_n.login_navn = tilganger.login_navn 
                and tilstand_n.oppgave = tilganger.oppgave
        ))
    """
    session.sql(sql).collect()
    sql = """
        update policies.login_navn_oppgave set _slettet_dato = current_date 
        where not exists (
            select 1 
            from policies.tilganger_oppgave tilganger
            where login_navn_oppgave.login_navn = tilganger.login_navn 
                and login_navn_oppgave.oppgave = tilganger.oppgave
        ) and _slettet_dato is null
    """
    session.sql(sql).collect()

