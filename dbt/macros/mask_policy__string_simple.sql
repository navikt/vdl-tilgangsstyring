{% macro mask_policy__string_simple() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            -- TODO: fjerne dette og lag struktur som sjekker hvilke ksted knyttet til aktuelle kunden
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when val is null then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__string_simple",
        val_type="string",
        body=body,
    ) %}
{% endmacro %}
