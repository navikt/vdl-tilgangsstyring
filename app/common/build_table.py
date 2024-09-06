from snowflake.snowpark.session import Session

def build_cost_centre_table(session: Session) -> None:
    sql = """
        create or replace table policies.login_navn_kostnadssted as
        with kostnadssteder as (
        select *
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
    #session.sql(sql).collect()

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

