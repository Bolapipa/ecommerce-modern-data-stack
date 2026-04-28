"""
Script responsável por gerar dados fictícios de e-commerce.

Este arquivo cria CSVs simulando dados de:
- clientes
- produtos
- pedidos
- itens dos pedidos
- pagamentos

Os arquivos gerados serão usados como fonte inicial do projeto.

Saída dos arquivos:
data/raw/
"""

import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker


# Pasta onde os arquivos CSV serão salvos.
# Exemplo final:
# data/raw/customers.csv
# data/raw/products.csv
OUTPUT_PATH = "data/raw"


# Quantidade de registros que queremos gerar.
# Você pode aumentar ou diminuir esses números depois.
TOTAL_CUSTOMERS = 200
TOTAL_PRODUCTS = 50
TOTAL_ORDERS = 500


# Inicializa o Faker em português do Brasil.
# Essa biblioteca gera nomes, e-mails, cidades e datas fictícias.
fake = Faker("pt_BR")


def create_output_folder() -> None:
    """
    Cria a pasta data/raw caso ela ainda não exista.

    Isso evita erro na hora de salvar os arquivos CSV.
    """
    os.makedirs(OUTPUT_PATH, exist_ok=True)


def generate_customers() -> pd.DataFrame:
    """
    Gera dados fictícios de clientes.

    Cada cliente terá:
    - id
    - nome
    - e-mail
    - cidade
    - estado
    - data de cadastro
    """

    # Lista onde vamos armazenar todos os clientes gerados.
    customers = []

    # Cria clientes de 1 até TOTAL_CUSTOMERS.
    for customer_id in range(1, TOTAL_CUSTOMERS + 1):
        customers.append(
            {
                # Identificador único do cliente.
                "customer_id": customer_id,

                # Nome fictício gerado pelo Faker.
                "customer_name": fake.name(),

                # E-mail fictício.
                "email": fake.email(),

                # Cidade fictícia.
                "city": fake.city(),

                # Sigla do estado, exemplo: RJ, SP, MG.
                "state": fake.estado_sigla(),

                # Data fictícia de cadastro nos últimos 2 anos.
                "created_at": fake.date_between(
                    start_date="-2y",
                    end_date="today"
                ),
            }
        )

    # Converte a lista de dicionários em um DataFrame pandas.
    return pd.DataFrame(customers)


def generate_products() -> pd.DataFrame:
    """
    Gera dados fictícios de produtos.

    Cada produto terá:
    - id
    - nome
    - categoria
    - preço
    """

    # Categorias fixas para os produtos.
    categories = ["Eletrônicos", "Casa", "Moda", "Esporte", "Livros", "Beleza"]

    # Lista onde vamos armazenar todos os produtos gerados.
    products = []

    # Cria produtos de 1 até TOTAL_PRODUCTS.
    for product_id in range(1, TOTAL_PRODUCTS + 1):
        products.append(
            {
                # Identificador único do produto.
                "product_id": product_id,

                # Nome fictício do produto.
                "product_name": fake.word().capitalize(),

                # Categoria escolhida aleatoriamente.
                "category": random.choice(categories),

                # Preço aleatório entre 20 e 1500, com 2 casas decimais.
                "price": round(random.uniform(20, 1500), 2),
            }
        )

    # Retorna os produtos como DataFrame.
    return pd.DataFrame(products)


def generate_orders(customers_df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera dados fictícios de pedidos.

    Cada pedido pertence a um cliente.

    Cada pedido terá:
    - id do pedido
    - id do cliente
    - data do pedido
    - status do pedido
    """

    # Status possíveis de um pedido.
    statuses = ["completed", "cancelled", "pending"]

    # Lista onde vamos armazenar todos os pedidos gerados.
    orders = []

    # Cria pedidos de 1 até TOTAL_ORDERS.
    for order_id in range(1, TOTAL_ORDERS + 1):

        # Cria uma data aleatória dentro dos últimos 365 dias.
        order_date = datetime.today() - timedelta(days=random.randint(0, 365))

        orders.append(
            {
                # Identificador único do pedido.
                "order_id": order_id,

                # Escolhe aleatoriamente um cliente existente.
                # Isso cria o relacionamento entre pedido e cliente.
                "customer_id": random.choice(
                    customers_df["customer_id"].tolist()
                ),

                # Data do pedido.
                "order_date": order_date.date(),

                # Status escolhido aleatoriamente.
                "status": random.choice(statuses),
            }
        )

    # Retorna os pedidos como DataFrame.
    return pd.DataFrame(orders)


def generate_order_items(
    orders_df: pd.DataFrame,
    products_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Gera dados fictícios dos itens dos pedidos.

    Um pedido pode ter mais de um item.

    Exemplo:
    Pedido 1:
    - Produto A, quantidade 2
    - Produto B, quantidade 1

    Cada item terá:
    - id do item
    - id do pedido
    - id do produto
    - quantidade
    - preço unitário
    """

    # Lista onde vamos armazenar todos os itens dos pedidos.
    order_items = []

    # Controle do identificador único do item do pedido.
    order_item_id = 1

    # Percorre todos os pedidos existentes.
    for order_id in orders_df["order_id"]:

        # Cada pedido terá entre 1 e 4 produtos.
        total_items = random.randint(1, 4)

        # Cria os itens daquele pedido.
        for _ in range(total_items):

            # Escolhe aleatoriamente um produto existente.
            product = products_df.sample(1).iloc[0]

            # Define uma quantidade aleatória entre 1 e 5.
            quantity = random.randint(1, 5)

            order_items.append(
                {
                    # Identificador único do item do pedido.
                    "order_item_id": order_item_id,

                    # Pedido ao qual esse item pertence.
                    "order_id": order_id,

                    # Produto comprado.
                    "product_id": int(product["product_id"]),

                    # Quantidade comprada.
                    "quantity": quantity,

                    # Preço do produto no momento da compra.
                    "unit_price": float(product["price"]),
                }
            )

            # Incrementa o id para o próximo item.
            order_item_id += 1

    # Retorna os itens dos pedidos como DataFrame.
    return pd.DataFrame(order_items)


def generate_payments(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera dados fictícios de pagamentos.

    Cada pedido terá um pagamento associado.

    Cada pagamento terá:
    - id do pagamento
    - id do pedido
    - método de pagamento
    - status do pagamento
    """

    # Formas de pagamento possíveis.
    payment_methods = ["credit_card", "pix", "boleto", "debit_card"]

    # Lista onde vamos armazenar os pagamentos.
    payments = []

    # Cria um pagamento para cada pedido.
    for payment_id, order_id in enumerate(orders_df["order_id"], start=1):
        payments.append(
            {
                # Identificador único do pagamento.
                "payment_id": payment_id,

                # Pedido relacionado ao pagamento.
                "order_id": order_id,

                # Método de pagamento escolhido aleatoriamente.
                "payment_method": random.choice(payment_methods),

                # Status do pagamento escolhido aleatoriamente.
                "payment_status": random.choice(
                    ["paid", "failed", "refunded"]
                ),
            }
        )

    # Retorna os pagamentos como DataFrame.
    return pd.DataFrame(payments)


def main() -> None:
    """
    Função principal do script.

    Ela executa o processo completo:
    1. cria a pasta de saída
    2. gera clientes
    3. gera produtos
    4. gera pedidos
    5. gera itens dos pedidos
    6. gera pagamentos
    7. salva tudo em arquivos CSV
    """

    # Garante que a pasta data/raw existe.
    create_output_folder()

    # Gera os dados principais.
    customers_df = generate_customers()
    products_df = generate_products()

    # Gera pedidos usando a lista de clientes.
    orders_df = generate_orders(customers_df)

    # Gera itens dos pedidos usando pedidos e produtos.
    order_items_df = generate_order_items(orders_df, products_df)

    # Gera pagamentos usando os pedidos.
    payments_df = generate_payments(orders_df)

    # Salva os DataFrames em arquivos CSV.
    # index=False evita salvar o índice do pandas como uma coluna extra.
    customers_df.to_csv(f"{OUTPUT_PATH}/customers.csv", index=False)
    products_df.to_csv(f"{OUTPUT_PATH}/products.csv", index=False)
    orders_df.to_csv(f"{OUTPUT_PATH}/orders.csv", index=False)
    order_items_df.to_csv(f"{OUTPUT_PATH}/order_items.csv", index=False)
    payments_df.to_csv(f"{OUTPUT_PATH}/payments.csv", index=False)

    # Mensagem final para confirmar que o script rodou corretamente.
    print("Arquivos CSV gerados com sucesso em data/raw/")


# Este bloco garante que a função main() só será executada
# quando este arquivo for rodado diretamente.
#
# Exemplo:
# python ingestion/generate_fake_data.py
if __name__ == "__main__":
    main()
