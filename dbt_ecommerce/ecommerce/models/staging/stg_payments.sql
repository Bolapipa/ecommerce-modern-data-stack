/*
    Modelo staging de pagamentos.

    Objetivo:
    - Ler os dados brutos da tabela raw.raw_payments
    - Converter os ids para número inteiro
    - Padronizar textos de método e status do pagamento
    - Preparar os dados para as próximas camadas
*/

WITH source_payments AS (

    SELECT
        payment_id,
        order_id,
        payment_method,
        payment_status
    FROM {{ source('raw', 'raw_payments') }}

),

staged_payments AS (

    SELECT
        CAST(payment_id AS INTEGER) AS payment_id,
        CAST(order_id AS INTEGER) AS order_id,
        LOWER(TRIM(payment_method)) AS payment_method,
        LOWER(TRIM(payment_status)) AS payment_status
    FROM source_payments

)

SELECT *
FROM staged_payments
