"""
Carrega os arquivos CSV de data/raw para tabelas no schema raw do PostgreSQL.
"""

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import connection as PgConnection


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "ecommerce")
POSTGRES_USER = os.getenv("POSTGRES_USER", "ecommerce_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "ecommerce_password")

TABLES_TO_LOAD = {
    "customers.csv": "raw_customers",
    "products.csv": "raw_products",
    "orders.csv": "raw_orders",
    "order_items.csv": "raw_order_items",
    "payments.csv": "raw_payments",
}


def get_connection() -> PgConnection:
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def create_raw_schema(connection: PgConnection) -> None:
    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")

    connection.commit()


def create_table_from_dataframe(connection: PgConnection, df: pd.DataFrame, table_name: str) -> None:
    with connection.cursor() as cursor:
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
            truncate_query = sql.SQL("TRUNCATE TABLE raw.{table_name};").format(
                table_name=sql.Identifier(table_name)
            )
            cursor.execute(truncate_query)
        else:
            columns_sql = [
                sql.SQL("{} TEXT").format(sql.Identifier(column_name))
                for column_name in df.columns
            ]

            create_table_query = sql.SQL(
                """
                CREATE TABLE raw.{table_name} (
                    {columns}
                );
                """
            ).format(
                table_name=sql.Identifier(table_name),
                columns=sql.SQL(", ").join(columns_sql),
            )

            cursor.execute(create_table_query)

    connection.commit()


def insert_dataframe(connection: PgConnection, df: pd.DataFrame, table_name: str) -> None:
    columns = list(df.columns)

    insert_query = sql.SQL(
        """
        INSERT INTO raw.{table_name} ({columns})
        VALUES ({values});
        """
    ).format(
        table_name=sql.Identifier(table_name),
        columns=sql.SQL(", ").join(map(sql.Identifier, columns)),
        values=sql.SQL(", ").join(sql.Placeholder() * len(columns)),
    )

    rows = [
        tuple(None if pd.isna(value) else str(value) for value in row)
        for row in df.to_numpy()
    ]

    with connection.cursor() as cursor:
        cursor.executemany(insert_query, rows)

    connection.commit()


def load_csv_to_postgres(connection: PgConnection, file_name: str, table_name: str) -> None:
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo nao encontrado: {file_path}")

    print(f"Carregando arquivo: {file_path}")
    df = pd.read_csv(file_path)

    create_table_from_dataframe(connection, df, table_name)
    insert_dataframe(connection, df, table_name)

    print(f"Tabela carregada com sucesso: raw.{table_name} ({len(df)} registros)")


def main() -> None:
    connection: PgConnection | None = None

    try:
        connection = get_connection()
        create_raw_schema(connection)

        for file_name, table_name in TABLES_TO_LOAD.items():
            load_csv_to_postgres(connection, file_name, table_name)

        print("Carga raw finalizada com sucesso.")

    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    main()
