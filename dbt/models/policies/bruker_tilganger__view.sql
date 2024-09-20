with 
    kostnadssteder as (select * from {{ ref('tilganger_kostnadssted') }}),
    oppgaver as (select * from {{ ref('tilganger_oppgave') }}),
    payload as (
        select 
            login_navn, 
            kostnadssted, 
            null as oppgave,
            gruppe_type
        from kostnadssteder
        union all
        select 
            login_navn, 
            null as kostnadssted,
            oppgave, 
            gruppe_type 
        from oppgaver
    ), final as (
        select * from payload
    )
select * 
from final 
order by 1 