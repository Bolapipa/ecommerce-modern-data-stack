"""
Script responsável por carregar os arquivos CSV da pasta data/raw
para o PostgreSQL.

Entrada:
- data/raw/customers.csv
- data/raw/products.csv
- data/raw/orders.csv
- data/raw/order_items.csv
- data/raw/payments.csv

Saída no PostgreSQL:
- raw.raw_customers
- raw.raw_products
- raw.raw_orders
- raw.raw_order_items
- raw.raw_payments
"""

import os

import pandas as pd
import psycopg2
from psycopg2 import sql


# Caminho onde estão os arquivos CSV gerados pelo script generate_fake_data.py
RAW_DATA_PATH = "data/raw"


# Configurações de conexão com o PostgreSQL.
# Aqui usamos localhost porque este script está rodando no seu PC,
# fora do container Docker.
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce")
POSTGRES_USER = os.getenv("POSTGRES_USER", "ecommerce_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ecommerce_password")


# Mapeamento entre arquivo CSV e tabela no PostgreSQL.
# Exemplo:
# customers.csv será carregado na tabela raw.raw_customers.
TABLES_TO_LOAD = {
    "customers.csv": "raw_customers",
    "products.csv": "raw_products",
    "orders.csv": "raw_orders",
    "order_items.csv": "raw_order_items",
    "payments.csv": "raw_payments",
}


def get_connection():
    """
    Cria uma conexão com o PostgreSQL.

    Essa conexão será usada para criar tabelas e inserir dados.
    """

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def create_raw_schema(connection) -> None:
    """
    Cria o schema raw caso ele ainda não exista.

    O schema raw é onde ficam os dados brutos.
    """

    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    connection.commit()


def create_table_from_dataframe(connection, df: pd.DataFrame, table_name: str) -> None:
    """
    Cria ou limpa uma tabela raw no PostgreSQL.

    Se a tabela ainda não existir:
    - cria a tabela com todas as colunas como TEXT.

    Se a tabela já existir:
    - limpa os dados com TRUNCATE TABLE.
    - não apaga a tabela, porque ela pode ter views do dbt dependendo dela.

    Por que não usamos DROP TABLE?
    - Porque as views staging do dbt dependem das tabelas raw.
    - Se tentarmos apagar a tabela raw, o PostgreSQL bloqueia a operação.
    """

    with connection.cursor() as cursor:
        # Verifica se a tabela já existe no schema raw
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_schema = 'raw'
                  AND table_name = %s
            );
            """,
            (table_name,),
        )

        table_exists = cursor.fetchone()[0]

        if table_exists:
            # Se a tabela já existe, apenas remove os dados antigos
            truncate_query = sql.SQL("""
                TRUNCATE TABLE raw.{table_name};
            """).format(
                table_name=sql.Identifier(table_name)
            )

            cursor.execute(truncate_query)

        else:
            # Se a tabela não existe, cria a estrutura com todas as colunas como TEXT
            columns_sql = []

            for column_name in df.columns:
                columns_sql.append(
                    sql.SQL("{} TEXT").format(sql.Identifier(column_name))
                )

            create_table_query = sql.SQL("""
                CREATE TABLE raw.{table_name} (
                    {columns}
                );
            """).format(
                table_name=sql.Identifier(table_name),
                columns=sql.SQL(", ").join(columns_sql),
            )

            cursor.execute(create_table_query)

    connection.commit()


def insert_dataframe(connection, df: pd.DataFrame, table_name: str) -> None:
    """
    Insere os dados do DataFrame na tabela PostgreSQL.

    A inserção é feita linha por linha para ficar mais simples de entender.
    Para volumes grandes, usaríamos uma estratégia mais performática,
    como COPY.
    """

    columns = list(df.columns)

    insert_query = sql.SQL("""
        INSERT INTO raw.{table_name} ({columns})
        VALUES ({values});
    """).format(
        table_name=sql.Identifier(table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
    )

    # Converte todos os valores para string ou None.
    # Isso combina com a decisão de criar todas as colunas como TEXT.
    rows = [
        tuple(None if pd.isna(value) else str(value) for value in row)
        for row in df.to_numpy()
    ]

    with connection.cursor() as cursor:
        cursor.executemany(insert_query, rows)

    connection.commit()


def load_csv_to_postgres(connection, file_name: str, table_name: str) -> None:
    """
    Lê um arquivo CSV e carrega seu conteúdo no PostgreSQL.
    """

    file_path = os.path.join(RAW_DATA_PATH, file_name)

    print(f"Carregando arquivo: {file_path}")

    df = pd.read_csv(file_path)

    create_table_from_dataframe(connection, df, table_name)
    insert_dataframe(connection, df, table_name)

    print(f"Tabela carregada com sucesso: raw.{table_name}")


def main() -> None:
    """
    Executa o processo completo de carga raw.

    Etapas:
    1. conecta no PostgreSQL
    2. cria o schema raw
    3. lê cada CSV
    4. cria a tabela correspondente
    5. insere os dados
    6. fecha a conexão
    """

    connection = get_connection()

    try:
        create_raw_schema(connection)

        for file_name, table_name in TABLES_TO_LOAD.items():
            load_csv_to_postgres(connection, file_name, table_name)

        print("Carga raw finalizada com sucesso.")

    finally:
        connection.close()


if __name__ == "__main__":
    main()
