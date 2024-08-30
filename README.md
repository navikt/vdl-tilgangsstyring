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
PS: her må Snowflake CLI connection objektet ```tilgangsstyring``` være definert ved å kjøre ```snow --info```og editere ```config.toml```-filen (dette må gjøres manuelt per nå).

## Hva virker ikke
- Oppdatering av tabeller i snowflake for å ha en oversikt over tilganger (user_login og kostnadssted/oppgave) som et resultat av hva brukere legger inn i appen. 

## TODOs
- Opprette tabeller, m.m. som streamlit appen trenger
    - view og __shared views__
- __Lage__ streamlit app 
- Snow CLI med Github actions
- __Lage__ dbt repo med ´row access policy´ macros
- Legge inn Snowflake CLI connection variabel som en del av miljøet? 


## Fjerning av Policies 
```sql
use database db; 
select distinct
'ALTER '||ref_entity_domain||
' '||ref_database_name||'.'||ref_schema_name||'.'||ref_entity_name||
' MODIFY COLUMN '||ref_column_name||
' UNSET MASKING POLICY;'
from table(information_schema.policy_references(policy_name=>'policies.<policy name>'));
```