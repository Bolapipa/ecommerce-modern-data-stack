/*
    Fato de itens dos pedidos.

    Objetivo:
    - Criar uma tabela final com os itens vendidos em cada pedido
    - Relacionar pedido, produto, quantidade e valores
    - Permitir análises de receita, volume vendido e produtos mais vendidos
*/

WITH order_items AS (

    SELECT
        order_item_id,
        order_id,
        product_id,
        quantity,
        unit_price,
        total_item_amount
    FROM {{ ref('stg_order_items') }}

),

orders AS (

    SELECT
        order_id,
        customer_id,
        order_date,
        order_status
    FROM {{ ref('stg_orders') }}

),

fact_order_items AS (

    SELECT
        order_items.order_item_id,
        order_items.order_id,
        orders.customer_id,
        order_items.product_id,
        orders.order_date,
        orders.order_status,
        order_items.quantity,
        order_items.unit_price,
        order_items.total_item_amount

    FROM order_items

    LEFT JOIN orders
        ON order_items.order_id = orders.order_id

)

SELECT *
FROM fact_order_items
