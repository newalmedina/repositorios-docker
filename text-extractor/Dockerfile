FROM python:3.11-slim

WORKDIR /app

# Copiamos requirements.txt desde la carpeta app
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido de la carpeta app al contenedor
COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
