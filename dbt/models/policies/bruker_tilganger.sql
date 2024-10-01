{{
    config(
        materialized="table",
    )
}}
with 
    source as (select * from {{ ref('beregnet_bruker_tilganger') }}),
    final as (
        select * from source
    )
select * from final
    
