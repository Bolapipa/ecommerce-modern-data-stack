# Ecommerce Modern Data Stack

Projeto de Engenharia de Dados para demonstrar um pipeline analitico completo com:
- ingestao em Python
- armazenamento em PostgreSQL
- transformacoes com dbt
- orquestracao com Dagster
- visualizacao no Metabase

Repositorio remoto: https://github.com/Bolapipa/ecommerce-modern-data-stack

## 1) Objetivo do projeto

O pipeline gera dados ficticios de e-commerce, carrega na camada `raw`, aplica transformacoes em camadas (`staging`, `intermediate`, `marts`) e disponibiliza tabelas finais para analise.

Fluxo de alto nivel:

```text
Python (geracao + carga)
        -> PostgreSQL (raw)
        -> dbt (staging/intermediate/marts)
        -> Metabase (dashboards)
Dagster orquestra todo o fluxo
```

## 2) Arquitetura

Camadas de dados:

```text
raw          dados brutos carregados dos CSVs
staging      tipagem, limpeza e padronizacao
intermediate joins e regras intermediarias
marts        tabelas finais para BI
```

Principais tabelas finais:
- `marts.dim_customers`
- `marts.dim_products`
- `marts.fact_orders`
- `marts.fact_order_items`
- `marts.sales_by_category`

## 3) Estrutura de pastas

```text
.
|-- ingestion/
|   |-- generate_fake_data.py
|   `-- load_raw_data.py
|-- orchestration/dagster_project/
|   |-- definitions.py
|   `-- Dockerfile
|-- dbt_ecommerce/ecommerce/
|   |-- dbt_project.yml
|   |-- profiles.yml
|   `-- models/
|-- dashboards/metabase/
|-- docs/
|-- docker-compose.yml
`-- requirements.txt
```

## 4) Pre-requisitos

- Docker Desktop
- Docker Compose
- Python 3.11+ (somente se for executar scripts fora do container)

## 5) Variaveis de ambiente

1. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

No Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

2. Revise os valores no `.env`:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=ecommerce_password
MB_DB_FILE=/metabase-data/metabase.db
DAGSTER_HOME=/opt/dagster/dagster_home
```

## 6) Subindo o ambiente com Docker

```bash
docker compose up -d --build
```

Servicos:
- PostgreSQL: `localhost:5432`
- Metabase: `http://localhost:3000`
- Dagster: `http://localhost:3001`

Verifique status:

```bash
docker compose ps
```

## 7) Executando o pipeline no Dagster

1. Abra `http://localhost:3001`
2. Materialize os assets na ordem (ou all assets):
- `generate_fake_data`
- `load_raw_data`
- `dbt_run`
- `dbt_test`
- `pipeline_summary`

Ao final, o arquivo `docs/pipeline_summary.txt` e gerado automaticamente.

## 8) Execucao manual (sem Dagster)

Se quiser rodar por etapas no seu ambiente Python local:

```bash
python ingestion/generate_fake_data.py
python ingestion/load_raw_data.py
```

Depois rode dbt:

```bash
cd dbt_ecommerce/ecommerce
dbt debug --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
```

## 9) dbt Docs (linhagem e documentacao)

Dentro de `dbt_ecommerce/ecommerce`:

```bash
dbt docs generate --profiles-dir .
dbt docs serve --port 8081 --profiles-dir .
```

Abra `http://localhost:8081`.

## 10) Metabase (analise)

1. Acesse `http://localhost:3000`
2. Conecte no PostgreSQL com as credenciais do `.env`
3. Explore tabelas no schema `marts`
4. Monte perguntas e dashboards

Screenshot de exemplo: `dashboards/metabase/screenshots/dashboard_ecommerce.png` (se aplicavel no seu ambiente)

## 11) Evidencias visuais ja presentes no projeto

- [Dagster pipeline sucesso](docs/dagster_pipeline_success.png)
- [Dagster lineage](docs/dagster_asset_lineage.png)
- [dbt lineage](docs/dbt_lineage.png)

## 12) Decisoes tecnicas

- A camada `raw` e carregada como `TEXT` para simplificar ingestao e tolerar variacoes de entrada.
- A tipagem e padronizacao ficam concentradas no `staging` (dbt).
- `orchestration/dagster_project/definitions.py` executa Python e dbt como etapas explicitamente separadas.
- `marts` contem tabelas prontas para consumo analitico.

## 13) Troubleshooting rapido

1. Erro de conexao no PostgreSQL
- Confirme `docker compose ps`
- Verifique se a porta `5432` esta livre
- Revise credenciais do `.env`

2. Script local nao encontra banco
- Se estiver rodando fora do Docker, use `POSTGRES_HOST=localhost`
- Se estiver rodando dentro do container Dagster, use `POSTGRES_HOST=postgres`

3. Falha no dbt por `profiles.yml`
- Rode dbt no diretorio `dbt_ecommerce/ecommerce`
- Confirme `--profiles-dir .`

4. Metabase sem tabelas
- Garanta que `dbt run` terminou com sucesso
- Confira se as tabelas foram criadas no schema `marts`

## 14) Roteiro de estudo sugerido

1. Rode o pipeline completo no Dagster.
2. Abra o dbt Docs e navegue na linhagem de `raw` ate `marts`.
3. Leia os modelos SQL em `models/staging` e `models/marts`.
4. Crie uma nova metrica no dbt (ex.: ticket medio por categoria).
5. Exponha a metrica em um dashboard no Metabase.

## 15) Proximos passos tecnicos

- Adicionar testes de relacionamento (chaves estrangeiras) no dbt
- Implementar CI para `dbt test` e validacao de SQL
- Evoluir ingestao para `COPY` no PostgreSQL para maior performance
