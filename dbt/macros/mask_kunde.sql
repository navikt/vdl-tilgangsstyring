{% macro mask_kunde() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when val is null then val
            when kunde_type != 'PERSON' then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_kunde",
        val_type="string",
        input_params=["kunde_type string"],
        body=body,
    ) %}
{% endmacro %}
