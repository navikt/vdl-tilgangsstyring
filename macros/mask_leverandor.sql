{% macro mask_leverandor() %}
    {% set body %}
        case
            when current_role() in ('REGNSKAP_TRANSFORMER','REPORTING_MICROSTRATEGY_GOD_MODE','REGNSKAP_LOADER' ) then val
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when val is null then val
            when er_organsiasjon then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do create_masking_policy(
        name="mask_leverandor",
        val_type="string",
        input_params=["er_organsiasjon boolean"],
        body=body,
    ) %}
{% endmacro %}
