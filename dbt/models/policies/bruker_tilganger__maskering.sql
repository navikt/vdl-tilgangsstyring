{{
    config(
        materialized="table",
    )
}}
with 
    source as (select * from {{ ref('beregnet_bruker_tilganger') }} where er_detalj_tilgang = TRUE),
    final as (
        select * from source
    )
select * from final
    
