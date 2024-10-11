{% macro mask_policy__string() %}
    {% set body %}
        case
            when val is null then val
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when exists (
            select 1 
            from tilgangsstyring.policies.bruker_tilganger__maskering 
            where login_navn = current_user() 
            and (kostnadssted = kostnadssted_kode or kostnadssted_gruppe = 'TOTAL')
            and (oppgave = oppgave_kode or oppgave_gruppe = 'TOTAL')
            and (artskonto = artskonto_kode or artskonto_gruppe = 'TOTAL')
            ) then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__string",
        val_type="string",
        input_params=["kostnadssted_kode string","oppgave_kode string", "artskonto_kode string"],
        body=body,
    ) %}
{% endmacro %}
