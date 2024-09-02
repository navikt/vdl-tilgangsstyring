from snowflake.snowpark.session import Session

def build_cost_centre_table(session: Session) -> None:
    sql = """
        create or replace table kostnadssteder as 
            select * 
            from tlost__oebs_prod.apps.xxrtv_gl_hierarki_v
            where flex_value_set_name = 'OR_KSTED' 
              and lower(hierarchy_code) = 'intern_ksted'
    """
    session.sql(sql).collect()
    sql = """
        create or replace table kostnadssted_hierarki as 
            with src as (
                select * 
                from kostnadssteder
            ), derived as (
                select 
                    flex_value as kostnadssted
                    , description as beskrivelse
                    , flex_value_parent as kostnadssted_forelder
                    , description_parent as forelder_beksrivelse
                from src
            ), recursive (
                kostnadssted
                , beskrivelse
                , kostnadssted_forelder
                , forelder_beksrivelse
                , n 
            ) as (
                select *
                    , 1 as n 
                from derived
                union all
                select 
                    derived.kostnadssted
                    , derived.beskrivelse
                    , recursive.kostnadssted_forelder
                    , recursive.forelder_beksrivelse
                    , recursive.n + 1 
                from derived 
                join recursive on derived.kostnadssted_forelder =  recursive.kostnadssted
                where recursive.kostnadssted_forelder is not null
            ) select * from recursive
    """
    session.sql(sql).collect()
    sql = """
        create or replace table policies.login_navn_kostnadssted as
        with kostnadssteder as (
        select 
            kostnadssted, 
            kostnadssted_forelder  
        from kostnadssted_hierarki
        union all 
        select distinct
            kostnadssted_forelder, 
            kostnadssted_forelder 
        from kostnadssted_hierarki
        ) select 
            users.login_name as login_navn, 
            kostnadssteder.kostnadssted
        from grupper
        join gruppe_kostnadssted_relasjoner relasjon on grupper.gruppe = relasjon.gruppe
        join gruppemedlemskap medlem on grupper.gruppe = medlem.gruppe
        join users on lower(users.email) = lower(medlem.epost)
        join kostnadssteder on kostnadssteder.kostnadssted_forelder = relasjon.kostnadssted
        order by 2
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
    session.sql(sql).collect()

