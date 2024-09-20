from snowflake.snowpark.session import Session

def load_access_table(session: Session) -> None:
    sql = """
        insert into policies.bruker_tilganger 
        select 
            login_navn,
            kostnadssted,
            oppgave,
            gruppe_type
        from policies.bruker_tilganger__view src
        where not exists (
            select 1 
            from policies.bruker_tilganger trgt
            where 
                src.login_navn=trgt.login_navn
                and src.kostnadssted=trgt.kostnadssted
                and src.oppgave=trgt.oppgave
                and src.gruppe_type=trgt.gruppe_type
        )
        order by 1 
    """
    session.sql(sql).collect()
    sql = """
        delete from policies.bruker_tilganger trgt
        where not exists (
            select 1 
            from policies.bruker_tilganger__view src 
            where 
                src.login_navn=trgt.login_navn
                and src.kostnadssted=trgt.kostnadssted
                and src.oppgave=trgt.oppgave
                and src.gruppe_type=trgt.gruppe_type
        ) 
    """
    session.sql(sql).collect()

