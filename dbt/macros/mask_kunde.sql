{% macro mask_kunde() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when exists ( select 1 from tilgangsstyring.policies.login_navn_kostnadssted where login_navn = current_user() and kostnadssted = kostnadssted_kode) then val

            when val is null then val
            when kunde_type != 'PERSON' then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_kunde",
        val_type="string",
        input_params=["kunde_type string", "kostnadssted_kode string"],
        body=body,
    ) %}
{% endmacro %}