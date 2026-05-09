# dbt Ecommerce Project

Projeto dbt da stack `ecommerce-modern-data-stack`.

## Estrutura de camadas

- `staging`: limpeza e tipagem dos dados raw
- `intermediate`: joins e enriquecimentos
- `marts`: tabelas finais para analise

## Comandos uteis

Rodar dentro deste diretorio (`dbt_ecommerce/ecommerce`):

```bash
dbt debug --profiles-dir .
dbt run --profiles-dir .
dbt test --profiles-dir .
```

## Documentacao

```bash
dbt docs generate --profiles-dir .
dbt docs serve --port 8081 --profiles-dir .
```

## Dependencia de ambiente

As credenciais do PostgreSQL sao lidas via variaveis de ambiente no `profiles.yml`.
