{{
    config(
        materialized="table",
    )
}}
with
    source as (
        select * from {{ ref("kostnadssteder") }}
    ), derived as (
        select 
              flex_value as kostnadssted
            , description as beskrivelse
            , flex_value_parent as kostnadssted_forelder
            , description_parent as forelder_beksrivelse
        from source
    ), recursive (
          kostnadssted
        , beskrivelse
        , kostnadssted_forelder
        , forelder_beskrivelse
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
            , recursive.forelder_beskrivelse
            , recursive.n + 1 
        from derived 
        join recursive on 
            derived.kostnadssted_forelder =  recursive.kostnadssted
        where recursive.kostnadssted_forelder is not null
    ), kostnadssteder as (
    select 
        kostnadssted_forelder,
        forelder_beskrivelse,
        kostnadssted,
        max(n) as n 
    from recursive 
    group by all
    ), 
    final as (
        select distinct 
            case when kostnadssted_forelder='T' then 'TOTAL' else kostnadssted_forelder end as gruppe
            , forelder_beskrivelse as gruppe_beskrivelse
            , case when kostnadssted_forelder='T' then null else kostnadssted end as kostnadssted 
            , n 
        from kostnadssteder
    )
select * 
from final