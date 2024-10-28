{{
    config(
        materialized="view",
    )
}}
with
    bruker_tilganger as (select * from {{ source("app", "bruker_tilganger") }}),
    kostnadssteder as (select * from {{ ref("kostnadssted_grupper") }}),
    kunder as (select * from {{ ref("kostnadssteder_kunde") }}),
    brukere as (select * from {{ source("app", "users") }}),
    bruker_tilganger_type as (
        select
            *,
            case
                when kostnadssted_gruppe = 'TOTAL' then 1 else 0
            end as har_alle_kunder_tilganger,
            rolle = 'DETALJE TILGANG' as er_detalj_tilganger
        from bruker_tilganger
    ),
    payload as (
        select distinct
            brukere.login_name as login_navn,
            max(har_alle_kunder_tilganger) har_alle_kunder_tilganger,
            arrayagg(distinct kunde_id) as kunde_id
        from bruker_tilganger_type
        join brukere on upper(brukere.email) = upper(bruker_tilganger_type.epost)
        join
            kostnadssteder
            on kostnadssteder.gruppe = bruker_tilganger_type.kostnadssted_gruppe
        left join 
            kunder on kunder.kostnadssted = kostnadssteder.kostnadssted
        where
            bruker_tilganger_type._slettet_dato is null
            and bruker_tilganger_type.fra_dato <= current_date
            and bruker_tilganger_type.til_dato > current_date
            and er_detalj_tilganger = 1
        group by all
    ),
    final as (select * from payload)
select *
from final
