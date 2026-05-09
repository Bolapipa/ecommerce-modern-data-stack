/*
    Mart de vendas por categoria.

    Objetivo:
    - Agrupar a receita por categoria de produto
    - Calcular quantidade vendida
    - Contar quantidade de pedidos
*/

WITH order_items AS (

    SELECT
        order_id,
        product_id,
        quantity,
        total_item_amount
    FROM {{ ref('fact_order_items') }}

),

products AS (

    SELECT
        product_id,
        category
    FROM {{ ref('dim_products') }}

),

sales_by_category AS (

    SELECT
        products.category,
        SUM(order_items.total_item_amount) AS total_revenue,
        SUM(order_items.quantity) AS total_quantity_sold,
        COUNT(DISTINCT order_items.order_id) AS total_orders

    FROM order_items

    LEFT JOIN products
        ON order_items.product_id = products.product_id

    GROUP BY
        products.category

)

SELECT *
FROM sales_by_category
