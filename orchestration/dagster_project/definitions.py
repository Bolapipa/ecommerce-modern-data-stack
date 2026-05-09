"""
Arquivo principal do Dagster.

Aqui definimos os assets do pipeline de dados.

Um asset no Dagster representa uma etapa que produz ou atualiza dados.

Neste projeto, o fluxo será:

1. generate_fake_data
2. load_raw_data
3. dbt_run
4. dbt_test
"""

import subprocess

from dagster import Definitions, asset


@asset
def generate_fake_data() -> None:
    """
    Gera arquivos CSV fictícios de e-commerce.

    Este asset executa o script:
    ingestion/generate_fake_data.py

    Saída esperada:
    data/raw/customers.csv
    data/raw/products.csv
    data/raw/orders.csv
    data/raw/order_items.csv
    data/raw/payments.csv
    """

    subprocess.run(
        ["python", "ingestion/generate_fake_data.py"],
        check=True,
    )


@asset(deps=[generate_fake_data])
def load_raw_data() -> None:
    """
    Carrega os arquivos CSV no PostgreSQL.

    Este asset executa o script:
    ingestion/load_raw_data.py

    Saída esperada no banco:
    raw.raw_customers
    raw.raw_products
    raw.raw_orders
    raw.raw_order_items
    raw.raw_payments
    """

    subprocess.run(
        ["python", "ingestion/load_raw_data.py"],
        check=True,
    )


@asset(deps=[load_raw_data])
def dbt_run() -> None:
    """
    Executa os modelos dbt.

    Este asset roda:
    dbt run

    Ele transforma os dados nas camadas:
    staging
    intermediate
    marts
    """

    subprocess.run(
        ["dbt", "run", "--profiles-dir", "."],
        cwd="dbt_ecommerce/ecommerce",
        check=True,
    )


@asset(deps=[dbt_run])
def dbt_test() -> None:
    """
    Executa os testes do dbt.

    Este asset roda:
    dbt test

    Ele valida regras de qualidade dos dados.
    """

    subprocess.run(
        ["dbt", "test", "--profiles-dir", "."],
        cwd="dbt_ecommerce/ecommerce",
        check=True,
    )


defs = Definitions(
    assets=[
        generate_fake_data,
        load_raw_data,
        dbt_run,
        dbt_test,
    ]
)
