{{
    config(
        materialized="view",
    )
}}
with
    bruker_tilganger as (select * from {{ source("app", "bruker_tilganger") }}),
    kostnadssteder as (select * from {{ ref("kostnadssted_grupper") }}),
    oppgaver as (select * from {{ source("app", "oppgave_grupper") }}),
    artskonti as (select * from {{ source("app", "artskonto_grupper") }}),
    brukere as (select * from {{ source("app", "users") }}),
    bruker_tilganger_type as (
        select
            *,
            case
                when kostnadssted_gruppe = 'TOTAL' then 1 else 0
            end as har_all_kostnadssteder,
            case when oppgave_gruppe = 'TOTAL' then 1 else 0 end as har_all_oppgaver,
            case when artskonto_gruppe = 'TOTAL' then 1 else 0 end as har_all_artskonti,
            rolle = 'DETALJE TILGANG' as er_detalj_tilganger
        from bruker_tilganger
    ),
    payload as (
        select distinct
            brukere.login_name as login_navn,
            er_detalj_tilganger,
            max(har_all_kostnadssteder) har_all_kostnadssteder,
            max(har_all_oppgaver) har_all_oppgaver,
            max(har_all_artskonti) har_all_artskonti,
            arrayagg(distinct kostnadssted) as kostnadssteder,
            arrayagg(distinct artskonto) as artskonti,
            arrayagg(distinct oppgave) as oppgaver
        from bruker_tilganger_type
        join
            kostnadssteder
            on kostnadssteder.gruppe = bruker_tilganger_type.kostnadssted_gruppe
        join oppgaver on oppgaver.gruppe = bruker_tilganger_type.oppgave_gruppe
        join artskonti on artskonti.gruppe = bruker_tilganger_type.artskonto_gruppe
        join brukere on upper(brukere.email) = upper(bruker_tilganger_type.epost)
        where
            bruker_tilganger_type._slettet_dato is null
            and bruker_tilganger_type.fra_dato <= current_date
            and bruker_tilganger_type.til_dato > current_date
        group by all
    ),
    final as (select * from payload)
select *
from final
