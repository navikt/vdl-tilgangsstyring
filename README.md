# vdl-streamlit

## Hvor finner jeg Appen 
App for tilgangsstyring ligger [her](https://app.snowflake.com/qqhhrqv/finansiell_styring/#/streamlit-apps/TILGANGSSTYRING_RAW.USER_INPUT.TILGANGSSTYRING).

## Deploy av Streamlit app
Aktivere miljø:
```shell
. ./setup_env.sh
```
Deploy Streamlit til Snowflake fra ```/app```
```shell 
snow streamlit deploy --connection tilgangsstyring --replace
```
PS: her må Snowflake CLI connection objektet ```tilgangsstyring``` være definert (dette må gjøres manuelt per nå).

## Hva virker ikke
- Oppdatering av tabeller i snowflake for å ha en oversikt over tilganger (user_login og kostnadssted/oppgave) som et resultat av hva brukere legger inn i appen. 

## TODOs
- Opprette tabeller, m.m. som streamlit appen trenger
    - view og __shared views__
- __Lage__ streamlit app 
- Snow CLI med Github actions
- __Lage__ dbt repo med ´row access policy´ macros
- Legge inn Snowflake CLI connection variabel som en del av miljøet? 