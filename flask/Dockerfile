# Base Python leve
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /flask

# Copia apenas requirements para acelerar cache
COPY requirements.txt .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . .

# Executa Gunicorn com 4 workers escutando na porta 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.main:app"]
