{% macro row_access__lite(policy_db, policy_schema) %}
    {% set body %}
        (
            (
                select max(har_all_kostnadssteder) 
                from tilgangsstyring.policies.bruker_tilganger__maskering 
                where login_navn = current_user
            ) = 1 
            or array_contains(kostnadssted_kode::variant,
                (
                    select kostnadssteder
                    from tilgangsstyring.policies.bruker_tilganger__maskering 
                    where login_navn = current_user
                )
            )
        ) and (
            (
                select max(har_all_oppgaver) 
                from tilgangsstyring.policies.bruker_tilganger__maskering 
                where login_navn = current_user
            ) = 1 
            or array_contains(oppgave_kode::variant,
                (
                    select oppgaver
                    from tilgangsstyring.policies.bruker_tilganger__maskering 
                    where login_navn = current_user
                )
            )
        ) and (
            (
                select max(har_all_artskonti) 
                from tilgangsstyring.policies.bruker_tilganger__maskering 
                where login_navn = current_user
            ) = 1 
            or array_contains(artskonto_kode::variant,
                (
                    select artskonti
                    from tilgangsstyring.policies.bruker_tilganger__maskering 
                    where login_navn = current_user
                )
            )
        ) or current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER'
    {% endset %}

    {% do vdl_macros.create_row_access_policy(
        name="row_access__lite",
        input_params=["kostnadssted_kode string","oppgave_kode string", "artskonto_kode string"],
        body=body,
    ) %}    
{% endmacro %}
