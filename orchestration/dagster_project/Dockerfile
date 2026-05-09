# Imagem base com Python 3.11
FROM python:3.11-slim

# Define a pasta principal dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias para algumas bibliotecas Python
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências para dentro do container
COPY requirements.txt .

# Instala as bibliotecas Python do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do projeto para dentro do container
COPY . .

# Define a pasta onde o Dagster guarda arquivos internos
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# Cria a pasta do Dagster
RUN mkdir -p $DAGSTER_HOME

# Comando padrão para iniciar a interface do Dagster
CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "orchestration/dagster_project/definitions.py"]
