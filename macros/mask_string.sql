{% macro mask_string() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when exists ( select 1 from tilgangsstyring.policies.login_navn_kostnadssted where login_navn = current_user() and kostnadssted = kostnadssted_kode) then val
            when val is null then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do create_masking_policy(
        name="mask_string",
        val_type="string",
        input_params=["kostnadssted_kode string"],
        body=body,
    ) %}
{% endmacro %}
