/*
    Modelo staging de clientes.

    Objetivo:
    - Ler os dados brutos da tabela raw.raw_customers
    - Padronizar os nomes das colunas
    - Converter os tipos de dados
    - Deixar a tabela pronta para ser usada nas próximas camadas
*/

WITH source_customers AS (

    SELECT
        customer_id,
        customer_name,
        email,
        city,
        state,
        created_at
    FROM {{ source('raw', 'raw_customers') }}

),

staged_customers AS (

    SELECT
        CAST(customer_id AS INTEGER) AS customer_id,
        TRIM(customer_name) AS customer_name,
        LOWER(TRIM(email)) AS email,
        TRIM(city) AS city,
        TRIM(state) AS state,
        CAST(created_at AS DATE) AS created_at
    FROM source_customers

)

SELECT *
FROM staged_customers
