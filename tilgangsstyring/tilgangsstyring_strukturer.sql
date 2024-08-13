use role tilgangsstyring_transformer;
use database tilgangsstyring_raw;
use schema user_input;

create table if not exists grupper(
    gruppe varchar(200),
    gruppe_beskrivelse varchar(1000),
    _opprettet_av varchar(40),
    _opprettet_date date,
    _oppdatert_av varchar(40),
    _oppdatert_date date,
    _slettet_date date
);

create table if not exists gruppe_kostnadssteds_relasjoner(
    gruppe varchar(200),
    kostandssteder varchar(200),
    _opprettet_av varchar(40),
    _opprettet_date date,
    _oppdatert_av varchar(40),
    _oppdatert_date date,
    _slettet_date date
);

create table if not exists gruppemeldemskap(
    gruppe varchar(200),
    epost varchar(200),
    fra_dato date,
    til_dato date,
    _opprettet_av varchar(40),
    _opprettet_date date,
    _oppdatert_av varchar(40),
    _oppdatert_date date,
    _slettet_date date
);

create or replace view gyldig_kostnadssted_liste as (
    select distinct 
        kostnadssteder_segment_kode_forelder as kostnadssteder
    from regnskap.intermediates.int_kostnadssteder_foreldre_relasjoner
);
create or replace view gyldige_oppgave_liste as
    select distinct 
        oppgaver_segment_kode as oppgave,
        oppgaver_segment_beskrivelse  as beskrivelse
    from regnskap.marts.dim_oppgaver;