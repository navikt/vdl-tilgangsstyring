{% macro row_access__join(policy_db, policy_schema) %}
join {policy_db}.{policy_schema}.bruker_tilganger on
(
    bruker_tilganger.login_navn = current_user() 
    and (bruker_tilganger.kostnadssted = final.kostnadssted 
    or bruker_tilganger.oppgave = final.oppgave
    ) and (
        (final.er_postert_pa_ytelse_konto=TRUE and bruker_tilganger.gruppe_type = 'YTELSE')
        or (final.er_postert_pa_ytelse_konto=FALSE and bruker_tilganger.gruppe_type = 'DRIFT')
        or (bruker_tilganger.gruppe_type = 'BEGGE')
    )
) or (current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER')
{% endmacro %}