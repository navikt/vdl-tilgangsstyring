{% macro row_access__kostnadssted_oppgave() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then true
            when exists ( select 1 from tilgangsstyring.policies.login_navn_kostnadssted where login_navn = current_user() and kostnadssted = kostnadssted_kode) then true
            when exists ( select 1 from tilgangsstyring.policies.login_navn_oppgave where login_navn = current_user() and oppgave = oppgave_kode) then true
            else false
        end
    {% endset %}

    {% do create_row_access_policy(
        name="row_access__kostnadssted_oppgave",
        input_params=["kostnadssted_kode string","oppgave_kode string"],
        body=body,
    ) %}    
{% endmacro %}
