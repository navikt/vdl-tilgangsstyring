{{
    config(
        materialized="view",
    )
}}
with
    bruker_tilganger as (select * from {{ source("app", "bruker_tilganger_kostnadssted") }}),
    --kostnadssteder as (select * from {{ ref("kostnadssted_grupper") }}),
    brukere as (select * from {{ source("app", "users") }}),
    bruker_tilganger_type as (
        select
            *,
            rolle = 'DETALJE TILGANG' as er_detalj_tilganger
        from bruker_tilganger
    ),
    payload as (
        select distinct
            brukere.login_name as login_navn,
            er_detalj_tilganger,
            kostnadsstedsniva,
            arrayagg(distinct kostnadssted_gruppe) as kostnadssteder
        from bruker_tilganger_type
        --join
        --    kostnadssteder
        --    on kostnadssteder.gruppe = bruker_tilganger_type.kostnadssted_gruppe
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
