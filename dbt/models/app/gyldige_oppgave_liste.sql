{{
    config(
        materialized="table",
    )
}}
with
    source as (select * from {{ source("oebs", "xxrtv_gl_segment_v") }}),

    payload as (
        select distinct
            flex_value as oppgave
            , description as oppgave_navn 
        from source
        where flex_value_set_name = 'OR_AKTIVITET' 
            and coalesce(end_date_active,to_timestamp('9999','yyyy')) >= to_timestamp('2023','yyyy')
            and enabled_flag = 'Y'
        order by 1
    ),

    final as (select * from payload)
select * from final