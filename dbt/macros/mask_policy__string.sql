{% macro mask_policy__string() %}
    {% set body %}
        case
            when exists (
                select 1 
                from tilgangsstyring.policies.bruker_tilganger 
                where login_navn = current_user() 
                and (kostnadssted = kostnadssted_kode 
                    or oppgave = oppgave_kode
                )
                and (
                    (er_ytelse=TRUE and gruppe_type = 'YTELSE')
                    or (er_ytelse=FALSE and gruppe_type = 'DRIFT')
                    or (gruppe_type = 'BEGGE')
                )
            ) or current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when val is null then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__string",
        val_type="string",
        input_params=["kostnadssted_kode string","oppgave_kode string", "er_ytelse boolean"],
        body=body,
    ) %}
{% endmacro %}
