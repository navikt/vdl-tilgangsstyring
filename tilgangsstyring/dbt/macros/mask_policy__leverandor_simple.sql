{% macro mask_policy__leverandor_simple() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            -- TODO: fjerne dette og lag struktur som sjekker hvilke ksted knyttet til aktuelle kunden
            when (select value from table(flatten(input => parse_json(current_available_roles()))) where value = 'REPORTING_MICROSTRATEGY_GOD_MODE') is not null then val
            when val is null then val
            when er_organsiasjon then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__leverandor_simple",
        val_type="string",
        input_params=["er_organsiasjon boolean"],
        body=body,
    ) %}
{% endmacro %}
