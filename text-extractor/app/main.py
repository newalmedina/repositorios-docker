from fastapi import FastAPI
from pydantic import BaseModel
import os
import openai
from dotenv import load_dotenv
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="IA Multi-Message Extractor OpenAI")

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
- Devolución del vehículo: fecha_hora_entrega, km_recorridos, combustible_entrega, combustible_devolucion, coste_extra, matricula_coche
- Cancelación: id_reserva, matricula_coche

Devuelve únicamente un JSON válido con los campos solicitados según el tipo de mensaje.
No agregues texto adicional.

Texto: {text}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        result_text = response.choices[0].message.content.strip()
    except Exception as e:
        return {"error": str(e)}

    try:
        result_json = json.loads(result_text)
    except json.JSONDecodeError:
        result_json = {"error": "No se pudo parsear JSON", "raw_output": result_text}

    return result_json
