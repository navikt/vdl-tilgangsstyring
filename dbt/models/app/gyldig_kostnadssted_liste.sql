{{
    config(
        materialized="table",
    )
}}
with

    source as (select * from {{ ref("kostnadssted_hierarki") }}),

    payload as (
        select distinct  
            kostnadssted
            , beskrivelse as kostnadssted_navn 
        from source
        order by 1
    ),

    final as ( select * from payload )

select * from final