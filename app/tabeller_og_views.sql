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
select * from tlost__oebs_prod.apps.xxrtv_gl_hierarki_v;
create or replace view xxrtv_gl_segment_v as 
select * from tlost__oebs_prod.apps.xxrtv_gl_segment_v;

use role securityadmin; 
grant create streamlit on schema tilgangsstyring.app to role tilgangsstyring_developer;

use role tilgangsstyring_developer;
use database tilgangsstyring;
use schema app;

create or replace view users as 
    select * 
    from snowflake_users.account_usage.users
;

create table if not exists bruker_tilganger__maskering(
    epost varchar(200),
    kostnadssted_gruppe varchar(200),
    oppgave_gruppe varchar(200),
    artskonto_gruppe varchar(200),
    er_detalj_tilgang boolean,
    begrunnelse varchar(2000), 
    fra_dato date,
    til_dato date,
    tilgang_gitt_av varchar(200),
    tilgang_gitt_fra timestamp,
    _slettet_dato timestamp
)
;

create table if not exists bruker_tilganger__filtreringcd (
    epost varchar(200),
    kostnadssted_gruppe varchar(200),
    oppgave_gruppe varchar(200),
    artskonto_gruppe varchar(200),
    er_detalj_tilgang boolean,
    begrunnelse varchar(2000), 
    fra_dato date,
    til_dato date,
    tilgang_gitt_av varchar(200),
    tilgang_gitt_fra timestamp,
    _slettet_dato timestamp
)
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