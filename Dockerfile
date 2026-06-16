# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Não gerar .pyc e não bufferizar a saída (logs aparecem na hora no docker logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY app/ ./app/

# Roda a aplicação com um usuário sem privilégios (boa prática de segurança)
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

# Verifica a saúde do container batendo no endpoint /health da própria API
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:5000/health', timeout=2).status == 200 else 1)"

# Em produção a API sobe com gunicorn (2 workers)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app.main:app"]
