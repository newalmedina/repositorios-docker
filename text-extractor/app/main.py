from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import json

app = FastAPI(title="IA Multi-Message Extractor")

# Modelo pequeño de Hugging Face
extractor = pipeline("text2text-generation", model="google/flan-t5-small")

class TextRequest(BaseModel):
    text: str

@app.post("/extract")
def extract_info(request: TextRequest):
    text = request.text

    prompt = f"""
    Analiza el siguiente mensaje relacionado con alquiler de coches.
    Detecta el tipo de mensaje (Confirmación, Comienzo, Devolución, Cancelación) y extrae los campos relevantes.

    Reglas:
    - Confirmación: fecha_inicio, fecha_fin, ingresos, id_reserva, matricula_coche
    - Comienzo del alquiler: km_entrega, combustible_entrega, arrendatario (nombre, telefono, email, carnet_conducir), matricula_coche
    - Devolución del vehículo: fecha_hora_entrega, km_recorridos, combustible_entrega, combustible_devolucion, coste_extra, matricula_coche (true/false)
    - Cancelación: id_reserva, matricula_coche

    Devuelve únicamente un JSON válido con los campos solicitados según el tipo de mensaje.
    No agregues texto adicional.

    Texto: {text}
    """

    result_text = extractor(prompt, max_length=512)[0]['generated_text']

    # Intentamos parsear JSON
    try:
        result_json = json.loads(result_text)
    except:
        result_json = {"error": "No se pudo parsear JSON", "raw_output": result_text}

    return result_json
