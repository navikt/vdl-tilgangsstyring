{% macro row_access__lite(policy_db, policy_schema) %}
    {% set body %}
        (
            array_contains(kostnadsstedsniva_0::variant,
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
        ) or current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER'
    {% endset %}

    {% do vdl_macros.create_row_access_policy(
        name="row_access__lite",
        input_params=[
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
