/*
    Fato de pedidos.

    Objetivo:
    - Criar uma tabela final com os pedidos do e-commerce
    - Guardar informações principais do pedido
    - Permitir análises por cliente, data, status e pagamento
*/

WITH orders_enriched AS (

    SELECT
        order_id,
        customer_id,
        order_date,
        order_status,
        payment_id,
        payment_method,
        payment_status
    FROM {{ ref('int_orders_enriched') }}

),

fact_orders AS (

    SELECT
        order_id,
        customer_id,
        order_date,
        order_status,
        payment_id,
        payment_method,
        payment_status,

        CASE
            WHEN order_status = 'completed' THEN 1
            ELSE 0
        END AS is_completed_order,

        CASE
            WHEN order_status = 'cancelled' THEN 1
            ELSE 0
        END AS is_cancelled_order

    FROM orders_enriched

)

SELECT *
FROM fact_orders
