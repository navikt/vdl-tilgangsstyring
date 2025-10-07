{% macro mask_policy__leverandor_string() %}
    {% set body %}
        case
            when val is null then val
            when er_organsiasjon then val
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when array_contains(kostnadsstedsniva_0::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_0')
                    )
                ) or 
                    array_contains(kostnadsstedsniva_1::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_1')
                    )
                ) or 
                    array_contains(kostnadsstedsniva_2::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_2')
                    )
                ) or 
                    array_contains(kostnadsstedsniva_3::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_3')
                    )
                ) or 
                    array_contains(kostnadsstedsniva_4::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_4')
                    )
                ) or 
                    array_contains(kostnadsstedsniva_5::variant,
                    (
                        select kostnadssteder
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                        and kostnadsstedsniva = upper('kostnadsstedsniva_5')
                    )
                )
            then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__leverandor_string",
        val_type="string",
        input_params=[
            "er_organsiasjon boolean",
            "kostnadsstedsniva_0 varchar",
            "kostnadsstedsniva_1 varchar",
            "kostnadsstedsniva_2 varchar",
            "kostnadsstedsniva_3 varchar",
            "kostnadsstedsniva_4 varchar",
            "kostnadsstedsniva_5 varchar",
        ],
        body=body,
    ) %}
{% endmacro %}
