use role accountadmin;
create or replace view snowflake_users.account_usage.users as 
    select login_name, email
    from snowflake.account_usage.users
    where not has_password;

use role sysadmin;
use database tilgangsstyring__raw;
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

create table if not exists grupper(
    gruppe varchar(200),
    gruppe_beskrivelse varchar(1000),
    gruppe_type varchar(200),
    _opprettet_av varchar(40),
    _opprettet_dato date,
    _oppdatert_av varchar(40),
    _oppdatert_dato date,
    _slettet_dato date
);

create table if not exists gruppe_kostnadssted_relasjoner(
    gruppe varchar(200),
    kostnadssted varchar(200),
    _opprettet_av varchar(40),
    _opprettet_dato date,
    _oppdatert_av varchar(40),
    _oppdatert_dato date,
    _slettet_dato date
);

create table if not exists gruppe_oppgave_relasjoner(
    gruppe varchar(200),
    oppgave varchar(200),
    _opprettet_av varchar(40),
    _opprettet_dato date,
    _oppdatert_av varchar(40),
    _oppdatert_dato date,
    _slettet_dato date
);

create table if not exists gruppemedlemskap(
    gruppe varchar(200),
    epost varchar(200),
    fra_dato date,
    til_dato date,
    _opprettet_av varchar(40),
    _opprettet_dato date,
    _oppdatert_av varchar(40),
    _oppdatert_dato date,
    _slettet_dato date
);

use schema policies;

create table if not exists login_navn_kostnadssted(
    login_navn varchar(200),
    kostnadssted varchar(200),
    _opprettet_dato date, 
    _slettet_dato date 
)
;
create table if not exists login_navn_oppgave(
    login_navn varchar(200),
    oppgave varchar(200),
    _opprettet_dato date, 
    _slettet_dato date 
)
;

