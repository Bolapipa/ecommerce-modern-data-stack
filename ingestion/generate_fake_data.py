"""
Gera dados ficticios de e-commerce e salva CSVs em data/raw.
"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"

TOTAL_CUSTOMERS = 200
TOTAL_PRODUCTS = 50
TOTAL_ORDERS = 500

fake = Faker("pt_BR")


def create_output_folder() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_customers() -> pd.DataFrame:
    customers = []

    for customer_id in range(1, TOTAL_CUSTOMERS + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": fake.name(),
                "email": fake.email(),
                "city": fake.city(),
                "state": fake.estado_sigla(),
                "created_at": fake.date_between(start_date="-2y", end_date="today"),
            }
        )

    return pd.DataFrame(customers)


def generate_products() -> pd.DataFrame:
    categories = ["Eletr\u00f4nicos", "Casa", "Moda", "Esporte", "Livros", "Beleza"]
    products = []

    for product_id in range(1, TOTAL_PRODUCTS + 1):
        products.append(
            {
                "product_id": product_id,
                "product_name": fake.word().capitalize(),
                "category": random.choice(categories),
                "price": round(random.uniform(20, 1500), 2),
            }
        )

    return pd.DataFrame(products)


def generate_orders(customers_df: pd.DataFrame) -> pd.DataFrame:
    statuses = ["completed", "cancelled", "pending"]
    customer_ids = customers_df["customer_id"].tolist()
    orders = []

    for order_id in range(1, TOTAL_ORDERS + 1):
        order_date = datetime.today() - timedelta(days=random.randint(0, 365))
        orders.append(
            {
                "order_id": order_id,
                "customer_id": random.choice(customer_ids),
                "order_date": order_date.date(),
                "status": random.choice(statuses),
            }
        )

    return pd.DataFrame(orders)


def generate_order_items(orders_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    order_items = []
    order_item_id = 1
    products = products_df.to_dict(orient="records")

    for order_id in orders_df["order_id"]:
        total_items = random.randint(1, 4)

        for _ in range(total_items):
            product = random.choice(products)
            quantity = random.randint(1, 5)

            order_items.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": int(product["product_id"]),
                    "quantity": quantity,
                    "unit_price": float(product["price"]),
                }
            )
            order_item_id += 1

    return pd.DataFrame(order_items)


def generate_payments(orders_df: pd.DataFrame) -> pd.DataFrame:
    payment_methods = ["credit_card", "pix", "boleto", "debit_card"]
    payment_statuses = ["paid", "failed", "refunded"]
    payments = []

    for payment_id, order_id in enumerate(orders_df["order_id"], start=1):
        payments.append(
            {
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_method": random.choice(payment_methods),
                "payment_status": random.choice(payment_statuses),
            }
        )

    return pd.DataFrame(payments)


def main() -> None:
    create_output_folder()

    customers_df = generate_customers()
    products_df = generate_products()
    orders_df = generate_orders(customers_df)
    order_items_df = generate_order_items(orders_df, products_df)
    payments_df = generate_payments(orders_df)

    customers_df.to_csv(OUTPUT_DIR / "customers.csv", index=False)
    products_df.to_csv(OUTPUT_DIR / "products.csv", index=False)
    orders_df.to_csv(OUTPUT_DIR / "orders.csv", index=False)
    order_items_df.to_csv(OUTPUT_DIR / "order_items.csv", index=False)
    payments_df.to_csv(OUTPUT_DIR / "payments.csv", index=False)

    print(f"Arquivos CSV gerados com sucesso em {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
