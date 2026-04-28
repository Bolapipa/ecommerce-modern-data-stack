/*
    Modelo intermediate de pedidos enriquecidos.

    Objetivo:
    - Juntar pedidos com clientes e pagamentos
    - Criar uma visão intermediária mais completa
    - Facilitar a criação das tabelas finais na camada marts
*/

WITH orders AS (

    SELECT
        order_id,
        customer_id,
        order_date,
        order_status
    FROM {{ ref('stg_orders') }}

),

customers AS (

    SELECT
        customer_id,
        customer_name,
        email,
        city,
        state
    FROM {{ ref('stg_customers') }}

),

payments AS (

    SELECT
        payment_id,
        order_id,
        payment_method,
        payment_status
    FROM {{ ref('stg_payments') }}

),

orders_enriched AS (

    SELECT
        orders.order_id,
        orders.customer_id,
        customers.customer_name,
        customers.email,
        customers.city,
        customers.state,
        orders.order_date,
        orders.order_status,
        payments.payment_id,
        payments.payment_method,
        payments.payment_status

    FROM orders

    LEFT JOIN customers
        ON orders.customer_id = customers.customer_id

    LEFT JOIN payments
        ON orders.order_id = payments.order_id

)

SELECT *
FROM orders_enriched
