{% macro mask_string() %}
    {% set body %}
        case
            when current_role() in ('REGNSKAP_TRANSFORMER','REPORTING_MICROSTRATEGY_GOD_MODE','REGNSKAP_LOADER' ) then val
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when val is null then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_string",
        val_type="string",
        body=body,
    ) %}
{% endmacro %}
