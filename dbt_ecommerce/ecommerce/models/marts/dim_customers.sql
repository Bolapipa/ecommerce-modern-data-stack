/*
    Dimensão de clientes.

    Objetivo:
    - Criar uma tabela final de clientes
    - Remover duplicidades
    - Manter apenas os campos úteis para análise
*/

WITH customers AS (

    SELECT
        customer_id,
        customer_name,
        email,
        city,
        state,
        created_at
    FROM {{ ref('stg_customers') }}

),

dim_customers AS (

    SELECT DISTINCT
        customer_id,
        customer_name,
        email,
        city,
        state,
        created_at
    FROM customers

)

SELECT *
FROM dim_customers
