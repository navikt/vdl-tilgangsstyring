{{
    config(
        materialized="table",
    )
}}
with

    source as (select * from {{ ref("kostnadssted_hierarki") }}),

    payload as (
        select distinct  
            kostnadssted_forelder as kostnadssted
            , forelder_beksrivelse as kostnadssted_navn 
        from source
        union all 
        select distinct  
            kostnadssted as kostnadssted
            , beskrivelse as kostnadssted_navn 
        from source
        order by 1
    ),

    final as ( select * from payload )

select * from final