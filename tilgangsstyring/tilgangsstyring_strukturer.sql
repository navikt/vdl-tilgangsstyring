use role tilgangsstyring_transformer;
use database tilgangsstyring_raw;
use schema user_input;

create table if not exists grupper(
    gruppe varchar(200),
    gruppe_beskrivelse varchar(1000),
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

create or replace view gyldig_kostnadssted_liste as (
    select distinct kostnadssted, kostnadssted_navn 
    from (
    select kostnadssteder_segment_kode_niva_1 as kostnadssted, kostnadssteder_segment_beskrivelse_niva_1 as kostnadssted_navn from regnskap.marts.dim_kostnadssteder
    union all
    select kostnadssteder_segment_kode_niva_2, kostnadssteder_segment_beskrivelse_niva_2 from regnskap.marts.dim_kostnadssteder
    union all
    select kostnadssteder_segment_kode_niva_3, kostnadssteder_segment_beskrivelse_niva_3 from regnskap.marts.dim_kostnadssteder
    union all
    select kostnadssteder_segment_kode_niva_4, kostnadssteder_segment_beskrivelse_niva_4 from regnskap.marts.dim_kostnadssteder
    )
);
create or replace view gyldige_oppgave_liste as
    select distinct 
        oppgaver_segment_kode as oppgave,
        oppgaver_segment_beskrivelse  as oppgave_navn
    from regnskap.marts.dim_oppgaver;