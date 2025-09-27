FROM python:3.11-slim

# Evitar mensajes de warning de apt
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instalar dependencias del sistema necesarias para spaCy
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY app/requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo de spaCy
RUN python -m spacy download en_core_web_sm

# Copiar la app
COPY app/ .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
