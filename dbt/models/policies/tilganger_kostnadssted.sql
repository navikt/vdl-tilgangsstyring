with 

kostnadssteder as (
    select * from {{ ref('kostnadssted_hierarki') }}
),

grupper as (
    select * from {{ source('app','grupper') }}
),

relasjon as (
    select * from {{ source('app','gruppe_kostnadssted_relasjoner') }}
),

medlem as (
    select * from {{ source('app','gruppemedlemskap') }}
),

users as (
    select * from {{ source('app','users') }}
),

payload as (
    select 
        users.login_name as login_navn, 
        kostnadssteder.kostnadssted, 
        grupper.gruppe_type
    from grupper
    join relasjon on grupper.gruppe = relasjon.gruppe
    join medlem on grupper.gruppe = medlem.gruppe
    join users on lower(users.email) = lower(medlem.epost)
    join kostnadssteder on kostnadssteder.kostnadssted_forelder = relasjon.kostnadssted
    where medlem.fra_dato <= current_date 
        and current_date <= medlem.til_dato
        and medlem._slettet_dato is null
        and relasjon._slettet_dato is null
        and grupper._slettet_dato is null
), 

final as (
    select * from payload
)

select * from final
