{{
    config(
        materialized="view",
    )
}}
with 
    bruker_tilganger as (select * from {{ source('app', 'bruker_tilganger') }}),
    kostnadssteder as (select * from {{ ref('kostnadssted_grupper') }}),
    oppgaver as (select * from {{ source('app', 'oppgave_grupper') }}),
    artskonti as (select * from {{ source('app', 'artskonto_grupper') }}),
    brukere as (select * from {{ source('app','users')}}),
    payload as (
        select 
            brukere.login_name as login_navn,
            kostnadssteder.gruppe as kostnadssted_gruppe,
            kostnadssteder.kostnadssted,
            oppgaver.gruppe as oppgave_gruppe,
            oppgaver.oppgave,
            artskonti.gruppe as artskonto_gruppe,
            artskonti.artskonto,
            bruker_tilganger.rolle
        from bruker_tilganger 
        join kostnadssteder on kostnadssteder.gruppe = bruker_tilganger.kostnadssted_gruppe
        join oppgaver on oppgaver.gruppe = bruker_tilganger.oppgave_gruppe
        join artskonti on artskonti.gruppe = bruker_tilganger.artskonto_gruppe
        join brukere on upper(brukere.email) = upper(bruker_tilganger.epost)
        where bruker_tilganger._slettet_dato is null   
          and bruker_tilganger.fra_dato <= current_date 
          and bruker_tilganger.til_dato > current_date 
    ),
    final as (
        select * from payload
    )
select * from final
    
