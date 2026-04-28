/*
    Modelo staging de produtos.

    Objetivo:
    - Ler os dados brutos da tabela raw.raw_products
    - Padronizar os nomes e textos
    - Converter os tipos de dados
    - Deixar os produtos prontos para as próximas camadas
*/

WITH source_products AS (

    SELECT
        product_id,
        product_name,
        category,
        price
    FROM {{ source('raw', 'raw_products') }}

),

staged_products AS (

    SELECT
        CAST(product_id AS INTEGER) AS product_id,
        TRIM(product_name) AS product_name,
        TRIM(category) AS category,
        CAST(price AS NUMERIC(10, 2)) AS price
    FROM source_products

)

SELECT *
FROM staged_products
