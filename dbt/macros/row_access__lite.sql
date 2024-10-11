{% macro row_access__lite(policy_db, policy_schema) %}
    {% set body %}
         exists (
            select 1 
            from tilgangsstyring.policies.bruker_tilganger__filtrering 
            where login_navn = current_user() 
            and (kostnadssted = kostnadssted_kode or kostnadssted_gruppe = 'TOTAL')
            and (oppgave = oppgave_kode or oppgave_gruppe = 'TOTAL')
            and (artskonto = artskonto_kode or artskonto_gruppe = 'TOTAL')
            ) or current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER'
    {% endset %}

    {% do vdl_macros.create_row_access_policy(
        name="row_access__lite",
        input_params=["kostnadssted_kode string","oppgave_kode string", "artskonto_kode string"],
        body=body,
    ) %}    
{% endmacro %}
