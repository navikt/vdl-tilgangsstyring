use role accountadmin;
create or replace view snowflake_users.account_usage.users as 
    select login_name, email
    from snowflake.account_usage.users
    where not has_password;


grant apply masking policy on account to role tilgangsstyring_admin;
grant apply row access policy on account to role tilgangsstyring_admin;

use role sysadmin;
use schema oebs;
create or replace view xxrtv_gl_hierarki_v  as 
select * from regnskap_raw.oebs.xxrtv_gl_hierarki_v__transient;
create or replace view xxrtv_gl_segment_v as 
select * from regnskap_raw.oebs.xxrtv_fist_gl_segment_v__transient;
create or replace view kostandssteder_kunde as 
select
ar.cust_account_id as kunde_id, 
bilag.segment2 as kostnadssted
from tlost__oebs_prod.apps.xxrtv_ar_transaksjons_v ar
join tlost__oebs_prod.apps.xxrtv_gl_bilag_v bilag on bilag.gl_sl_link_id = ar.gl_sl_link_id 
and bilag.gl_sl_link_table = ar.gl_sl_link_table
;
use role securityadmin; 
grant create streamlit on schema tilgangsstyring.app to role tilgangsstyring_developer;

use role tilgangsstyring_developer;
use database tilgangsstyring;
use schema app;

create or replace view users as 
    select * 
    from snowflake_users.account_usage.users
;

use warehouse tilgangsstyring_app
;

create table if not exists oppgave_grupper as
select 
    cast('TOTAL' as varchar(200)) as gruppe,
    cast('Total i NAV' as varchar(200)) as gruppe_beskrivelse,
    cast(NULL as varchar(200)) as oppgave,
    cast(NULL as varchar(2000)) as oppgave_beskrivelse
;

create table if not exists artskonto_grupper as
select 
    cast('TOTAL' as varchar(200)) as gruppe, 
    cast('Total i NAV' as varchar(200)) as gruppe_beskrivelse,
    cast(NULL as varchar(200)) as artskonto, 
    cast(NULL as varchar(2000)) as artskonto_beskrivelse
;