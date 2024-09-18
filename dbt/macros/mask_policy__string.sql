{% macro mask_policy__string() %}
    {% set body %}
        case
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when exists ( select 1 from tilgangsstyring.policies.login_navn_kostnadssted where login_navn = current_user() and kostnadssted = kostnadssted_kode) then val
            when val is null then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__string",
        val_type="string",
        input_params=["kostnadssted_kode string"],
        body=body,
    ) %}
{% endmacro %}
