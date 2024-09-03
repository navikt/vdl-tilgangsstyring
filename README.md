# vdl-streamlit

## Hvor finner jeg appen 
App for tilgangsstyring ligger [her](https://app.snowflake.com/qqhhrqv/finansiell_styring/#/streamlit-apps/TILGANGSSTYRING_RAW.USER_INPUT.TILGANGSSTYRING).

## Deploy av app
Aktivere miljø:
```shell
. ./setup_env.sh
```
Fra root kjør 
```shell
snowbird run
snow sql -f app/tabeller_og_views.sql  --connection <connection>
```
PS: her må Snowflake CLI connection objektet ```<connection>``` være definert ved å kjøre ```snow --info```og editere ```config.toml```-filen (dette må gjøres manuelt per nå).

Deploy Streamlit til Snowflake fra ```/app```
```shell 
cd app
snow streamlit deploy --connection <connection> --replace
snow sql -f post_hook.sql --connection <connection>
```



## TODOs
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