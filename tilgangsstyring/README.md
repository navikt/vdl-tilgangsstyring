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

## Legge til brukere manuelt 
Når du skal tildele brukere __av-maskering__ kjører du følgende script
```sql
insert into tilgangsstyring.app.bruker_tilganger_kostnadssted
with vw as (
select '<navn@nav.no>' as epost
--union all
--select '<navn@nav.no>' as epost
)
select 
initcap(epost),
'<kostandsstedsnivå>',
'KOSTNADSSTEDSNIVA_<n>',
'DETALJE TILGANG' ,
'<begrunnelse>',
to_date('<fra år>-12-01','yyyy-mm-dd'),
to_date('<til år>-12-31','yyyy-mm-dd'),
'<din epostadresse>',
current_timestamp,
null
from vw
;
```
Så kjører du `dbt build` mot `tilgangsstyring`-miljøet. 

## Fjerning av Policies 
Slik fjerner du og rydder opp i policies
```sql
use database db; 
select distinct
'ALTER '||ref_entity_domain||
' '||ref_database_name||'.'||ref_schema_name||'.'||ref_entity_name||
' MODIFY COLUMN '||ref_column_name||
' UNSET MASKING POLICY;'
from table(information_schema.policy_references(policy_name=>'policies.<policy name>'));
```