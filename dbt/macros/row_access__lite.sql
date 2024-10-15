{% macro row_access__lite(policy_db, policy_schema) %}
    {% set body %}
         (
            (
                (
                    select max(har_all_kostnadssteder) 
                    from tilgangsstyring.policies.bruker_tilganger__filtrering 
                    where login_navn = current_user
                ) = 1 
                or contains(
                    (
                        select max(kostnadssteder) 
                        from tilgangsstyring.policies.bruker_tilganger__filtrering 
                        where login_navn = current_user
                    ), kostnadssted_kode
                )
            ) and (
                (
                    select max(har_all_oppgaver) 
                    from tilgangsstyring.policies.bruker_tilganger__filtrering 
                    where login_navn = current_user
                ) = 1 
                or contains(
                    (
                        select max(oppgaver) 
                        from tilgangsstyring.policies.bruker_tilganger__filtrering 
                        where login_navn = current_user
                    ), oppgave_kode
                )
            ) and (
                (
                    select max(har_all_artskonti) 
                    from tilgangsstyring.policies.bruker_tilganger__filtrering 
                    where login_navn = current_user
                ) = 1 
                or contains(
                    (
                        select max(artskonti) 
                        from tilgangsstyring.policies.bruker_tilganger__filtrering 
                        where login_navn = current_user
                    ), artskonto_kode
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
