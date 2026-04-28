/*
    Dimensão de produtos.

    Objetivo:
    - Criar uma tabela final de produtos
    - Remover duplicidades
    - Manter os campos úteis para análise
*/

WITH products AS (

    SELECT
        product_id,
        product_name,
        category,
        price
    FROM {{ ref('stg_products') }}

),

dim_products AS (

    SELECT DISTINCT
        product_id,
        product_name,
        category,
        price
    FROM products

)

SELECT *
FROM dim_products
