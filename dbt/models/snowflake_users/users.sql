with 

source as (
    select * from {source('snowflake','users')}
),

derived_colums as (
    select login_name, email
    from source
    where not has_password;
),

final as (
    select * from derived_colums
)
select * from final