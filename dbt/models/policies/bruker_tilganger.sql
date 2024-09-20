{{
    config(
        materialized="table",
    )
}}
with 
    bruker_tilganger as (
        select * from {{ ref('bruker_tilganger__view') }}
    ),  final as (
        select * from bruker_tilganger
    )
select * 
from final 
order by login_navn