/*
    Modelo staging de itens dos pedidos.

    Objetivo:
    - Ler os dados brutos da tabela raw.raw_order_items
    - Converter ids e valores numéricos
    - Criar o valor total de cada item do pedido
    - Preparar os dados para a camada de marts

    Observação:
    - Alguns valores chegam como texto decimal, exemplo: '47.0'
    - Por isso, primeiro convertemos para NUMERIC
    - Depois convertemos para INTEGER quando necessário
*/

WITH source_order_items AS (

    SELECT
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price
    FROM {{ source('raw', 'raw_order_items') }}

),

staged_order_items AS (

    SELECT
        CAST(CAST(order_item_id AS NUMERIC) AS INTEGER) AS order_item_id,
        CAST(CAST(order_id AS NUMERIC) AS INTEGER) AS order_id,
        CAST(CAST(product_id AS NUMERIC) AS INTEGER) AS product_id,
        CAST(CAST(quantity AS NUMERIC) AS INTEGER) AS quantity,

        CAST(unit_price AS NUMERIC(10, 2)) AS unit_price,

        CAST(CAST(quantity AS NUMERIC) AS INTEGER)
            * CAST(unit_price AS NUMERIC(10, 2)) AS total_item_amount

    FROM source_order_items

)

SELECT *
FROM staged_order_items
