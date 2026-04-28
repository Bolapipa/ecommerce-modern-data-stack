/*
    Macro para controlar o nome dos schemas criados pelo dbt.

    Por padrão, o dbt junta:
    schema do profiles.yml + schema do dbt_project.yml

    Exemplo ruim:
    staging + marts = staging_marts

    Com esta macro, o dbt vai usar exatamente o schema definido
    no dbt_project.yml.

    Exemplo correto:
    marts = marts
*/

{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if custom_schema_name is none -%}

        {{ target.schema }}

    {%- else -%}

        {{ custom_schema_name | trim }}

    {%- endif -%}

{%- endmacro %}
