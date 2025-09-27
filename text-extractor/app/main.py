from fastapi import FastAPI
from pydantic import BaseModel
import re
import spacy

app = FastAPI(title="Text Extractor Gratis y Robusto")

# Cargamos spaCy en inglés y español
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")

class TextRequest(BaseModel):
    text: str

# Detectar tipo de mensaje con palabras clave
def detect_tipo(text):
    lower = text.lower()
    if "reserva confirmada" in lower:
        return "Confirmación"
    elif "contrato de alquiler - comienzo" in lower:
        return "Comienzo"
    elif "contrato de alquiler - devolución" in lower:
        return "Devolución"
    elif "ha cancelado tu reserva" in lower:
        return "Cancelación"
    else:
        return "Desconocido"

# Funciones de extracción
def extract_confirmacion(text):
    data = {}
    # Fechas
    fechas = re.findall(r'\d{1,2}\.\s*\w+\s*\d{0,4}\s*a\s*las\s*\d{1,2}:\d{2}', text)
    if len(fechas) >= 2:
        data["fecha_inicio"] = fechas[0]
        data["fecha_fin"] = fechas[1]
    # Ingresos
    ingresos = re.search(r'Ingresos totales\s*([\d,.]+)', text)
    if ingresos:
        data["ingresos"] = ingresos.group(1)
    # ID reserva
    id_reserva = re.search(r'ID de reserva\s*(\d+)', text)
    if id_reserva:
        data["id_reserva"] = id_reserva.group(1)
    # Matrícula
    matricula = re.search(r'\b[A-Z0-9]{4,8}\b', text)
    if matricula:
        data["matricula_coche"] = matricula.group(0)
    return data

def extract_comienzo(text):
    data = {}
    # Matrícula
    matricula = re.search(r'\b[A-Z0-9]{4,8}\b', text)
    if matricula:
        data["matricula_coche"] = matricula.group(0)
    # km entrega
    km = re.search(r'Kilometraje a la entrega\s*(\d+)', text)
    if km:
        data["km_entrega"] = km.group(1)
    # combustible
    combustible = re.search(r'Nivel a la entrega\s*(\d+%)', text)
    if combustible:
        data["combustible_entrega"] = combustible.group(1)
    # Arrendatario
    arrendatario = {}
    nombre_match = re.search(r'Arrendatario\s+Nombre\s+(.+?)\s+Teléfono', text, re.DOTALL)
    if nombre_match:
        arrendatario["nombre"] = nombre_match.group(1).strip()
    telefono_match = re.search(r'Teléfono\s+(\d+)', text)
    if telefono_match:
        arrendatario["telefono"] = telefono_match.group(1).strip()
    email_match = re.search(r'Email\s+(\S+)', text)
    if email_match:
        arrendatario["email"] = email_match.group(1).strip()
    carnet_match = re.search(r'Número del carne de conducir\s+(\S+)', text)
    if carnet_match:
        arrendatario["carnet_conducir"] = carnet_match.group(1).strip()
    if arrendatario:
        data["arrendatario"] = arrendatario
    return data

def extract_devolucion(text):
    data = {}
    matricula = re.search(r'\b[A-Z0-9]{4,8}\b', text)
    if matricula:
        data["matricula_coche"] = matricula.group(0)
    fecha_entrega = re.search(r'Fecha y hora\s*(\d{1,2}\.\s*\w+\s*\d{0,4}\s*a\s*\d{1,2}:\d{2})', text)
    if fecha_entrega:
        data["fecha_hora_entrega"] = fecha_entrega.group(1)
    km = re.search(r'Kilómetros recorridos\s*(\d+)', text)
    if km:
        data["km_recorridos"] = km.group(1)
    combustible_entrega = re.search(r'Nivel a la entrega\s*(\d+%)', text)
    if combustible_entrega:
        data["combustible_entrega"] = combustible_entrega.group(1)
    combustible_dev = re.search(r'Nivel a la devolución\s*(\d+%)', text)
    if combustible_dev:
        data["combustible_devolucion"] = combustible_dev.group(1)
    data["coste_extra"] = bool(re.search(r'Costes extra', text, re.IGNORECASE))
    return data

def extract_cancelacion(text):
    data = {}
    id_reserva = re.search(r'ID de reserva\s*(\d+)', text)
    if id_reserva:
        data["id_reserva"] = id_reserva.group(1)
    matricula = re.search(r'\b[A-Z0-9]{4,8}\b', text)
    if matricula:
        data["matricula_coche"] = matricula.group(0)
    return data

@app.post("/extract")
def extract_info(request: TextRequest):
    text = request.text
    tipo = detect_tipo(text)
    if tipo == "Confirmación":
        data = extract_confirmacion(text)
    elif tipo == "Comienzo":
        data = extract_comienzo(text)
    elif tipo == "Devolución":
        data = extract_devolucion(text)
    elif tipo == "Cancelación":
        data = extract_cancelacion(text)
    else:
        data = {"error": "Tipo de mensaje desconocido"}
    data["tipo_mensaje"] = tipo
    return data
