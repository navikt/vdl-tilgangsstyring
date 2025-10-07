{% macro mask_policy__kunde() %}
    {% set body %}
        case
            when val is null then val
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when (
                (
                    select max(har_alle_kunder_tilganger) 
                    from tilgangsstyring.policies.bruker_tilganger__kunde_maskering 
                    where login_navn = current_user
                ) = 1 
                or array_contains(kunde_id_kode::variant,
                    (
                        select kunde_id
                        from tilgangsstyring.policies.bruker_tilganger__kunde_maskering 
                        where login_navn = current_user
                    )
                )
            ) then val
            when kunde_type != 'PERSON' then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__kunde",
        val_type="string",
        input_params=[
            "kunde_type string",
            "kunde_id_kode string",
        ],
        body=body,
    ) %}
{% endmacro %}
