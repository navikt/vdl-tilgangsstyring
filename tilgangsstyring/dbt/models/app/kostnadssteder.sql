{{
    config(
        materialized="table",
    )
}}
with
    source as (select * from {{ source("oebs", "xxrtv_gl_hierarki_v") }}),

    payload as (
        select * 
        from source
        where flex_value_set_name = 'OR_KSTED' 
          and lower(hierarchy_code) = 'intern_ksted'
    ),

    final as (select * from payload)

select * from final