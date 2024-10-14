{% macro mask_policy__string() %}
    {% set body %}
        case
            when val is null then val
            when current_role() like '%_TRANSFORMER' or current_role() like '%_LOADER' then val
            when (
                (
                    select max(har_all_kostnadssteder) 
                    from tilgangsstyring.policies.bruker_tilganger__maskering 
                    where login_navn = current_user
                ) = 1 
                or contains(
                    kostnadssted_kode, 
                    (
                        select max(kostnadssteder) 
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
                or contains(
                    oppgave_kode, 
                    (
                        select max(oppgaver) 
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
                or contains(
                    artskonto_kode, 
                    (
                        select max(artskonti) 
                        from tilgangsstyring.policies.bruker_tilganger__maskering 
                        where login_navn = current_user
                    )
                )
            ) then val
            else '* MASKERT *'
        end
    {% endset %}

    {% do vdl_macros.create_masking_policy(
        name="mask_policy__string",
        val_type="string",
        input_params=[
            "kostnadssted_kode string",
            "oppgave_kode string",
            "artskonto_kode string",
        ],
        body=body,
    ) %}
{% endmacro %}
