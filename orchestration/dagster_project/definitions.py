"""
Arquivo principal do Dagster.

Define os assets:
1. generate_fake_data
2. load_raw_data
3. dbt_run
4. dbt_test
5. pipeline_summary
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dagster import Definitions, asset


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DBT_PROJECT_DIR = PROJECT_ROOT / "dbt_ecommerce" / "ecommerce"
DOCS_DIR = PROJECT_ROOT / "docs"


def run_command(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        check=True,
    )


@asset
def generate_fake_data() -> None:
    run_command([sys.executable, str(PROJECT_ROOT / "ingestion" / "generate_fake_data.py")])


@asset(deps=[generate_fake_data])
def load_raw_data() -> None:
    run_command([sys.executable, str(PROJECT_ROOT / "ingestion" / "load_raw_data.py")])


@asset(deps=[load_raw_data])
def dbt_run() -> None:
    run_command(["dbt", "run", "--profiles-dir", "."], cwd=DBT_PROJECT_DIR)


@asset(deps=[dbt_run])
def dbt_test() -> None:
    run_command(["dbt", "test", "--profiles-dir", "."], cwd=DBT_PROJECT_DIR)


@asset(deps=[dbt_test])
def pipeline_summary() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    summary_text = f"""
Pipeline executado com sucesso.

Etapas executadas:
1. Geracao de dados fake
2. Carga raw no PostgreSQL
3. Transformacoes dbt
4. Testes dbt
5. Geracao deste resumo

Data/hora da execucao: {execution_time}
""".strip()

    output_file = DOCS_DIR / "pipeline_summary.txt"
    output_file.write_text(summary_text, encoding="utf-8")

    print(f"Resumo do pipeline criado em {output_file}")


defs = Definitions(
    assets=[
        generate_fake_data,
        load_raw_data,
        dbt_run,
        dbt_test,
        pipeline_summary,
    ]
)
