/*
    Modelo staging de pedidos.

    Objetivo:
    - Ler os dados brutos da tabela raw.raw_orders
    - Converter os campos para os tipos corretos
    - Padronizar o status do pedido
    - Preparar os dados para as camadas intermediate e marts
*/

WITH source_orders AS (

    SELECT
        order_id,
        customer_id,
        order_date,
        status
    FROM {{ source('raw', 'raw_orders') }}

),

staged_orders AS (

    SELECT
        CAST(order_id AS INTEGER) AS order_id,
        CAST(customer_id AS INTEGER) AS customer_id,
        CAST(order_date AS DATE) AS order_date,
        LOWER(TRIM(status)) AS order_status
    FROM source_orders

)

SELECT *
FROM staged_orders
