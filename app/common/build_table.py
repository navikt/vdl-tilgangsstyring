from snowflake.snowpark.session import Session

def build_cost_centre_table(session: Session) -> None:
    sql = """
        create or replace table policies.login_navn_kostnadssted as
        with kostnadssteder as (
        select * 
        from regnskap.marts.dim_kostnadssteder_utflatet
        union all 
        select distinct
            kostnadssteder_segment_kode_forelder, 
            kostnadssteder_segment_kode_forelder 
        from regnskap.marts.dim_kostnadssteder_utflatet
        ) select 
            users.login_name as login_navn, 
            kostnadssteder.kostnadssteder_segment_kode as kostnadssted
        from grupper
        join gruppe_kostnadssted_relasjoner relasjon on grupper.gruppe = relasjon.gruppe
        join gruppemedlemskap medlem on grupper.gruppe = medlem.gruppe
        join users on lower(users.email) = lower(medlem.epost)
        join kostnadssteder on kostnadssteder.kostnadssteder_segment_kode_forelder = relasjon.kostnadssted
    """

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

