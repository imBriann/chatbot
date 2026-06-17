import requests
import json
import uuid

BASE_URL = "http://127.0.0.1:8001/api"
SESSION_ID = str(uuid.uuid4())

PREGUNTAS = [
    "¿Cuándo son las fechas de inscripción?",
    "¿Cómo es el proceso para inscribirme en línea?",
    "¿Qué documentos o requisitos me piden para la admisión?",
    "¿Cuáles son los requisitos para estudiantes extranjeros?",
    "¿Cómo funciona la movilidad académica o los intercambios?",
    "¿Quién asume los costos de una movilidad internacional?",
    "¿De cuánto es el valor del semestre o matrícula?",
    "¿Qué becas o apoyos económicos ofrece la universidad?",
    "¿Cuáles son los descuentos disponibles para la matrícula?",
    "¿Aplica el beneficio de matrícula cero?",
    "¿Cuáles son los requisitos para poderme graduar?",
    "¿Cuándo se realizan las ceremonias de grado?",
    "¿Dónde quedan ubicadas las diferentes sedes?",
    "¿Qué servicios de salud y apoyo brinda Bienestar Universitario?",
    "¿Qué programas de pregrado ofrece la universidad?"
]

def main():
    print("Iniciando pruebas de las 15 preguntas mediante la API...")
    resultados = []
    
    for i, q in enumerate(PREGUNTAS, 1):
        print(f"Probando {i}/15: {q}")
        try:
            resp = requests.post(
                f"{BASE_URL}/chat/message",
                json={"sessionId": SESSION_ID, "message": q},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json()
                resultados.append({
                    "num": i,
                    "pregunta": q,
                    "respuesta": data.get("response", ""),
                    "confidence": data.get("confidence", 0.0),
                    "status": "PASSED" if data.get("confidence", 0.0) >= 0.5 else "LOW_CONFIDENCE"
                })
            else:
                resultados.append({
                    "num": i,
                    "pregunta": q,
                    "respuesta": f"Error del servidor HTTP {resp.status_code}",
                    "confidence": 0.0,
                    "status": "FAILED"
                })
        except Exception as e:
            resultados.append({
                "num": i,
                "pregunta": q,
                "respuesta": f"Excepción de conexión: {str(e)}",
                "confidence": 0.0,
                "status": "FAILED"
            })
            
    # Guardar en un markdown intermedio para leerlo
    with open("resultado_15_preguntas.md", "w", encoding="utf-8") as f:
        f.write("# 📋 Resultados Detallados de las 15 Preguntas del Chat\n\n")
        f.write("| # | Pregunta | Respuesta del Chatbot | Confianza | Estado |\n")
        f.write("|---|---|---|:---:|:---:|\n")
        for r in resultados:
            # Reemplazar saltos de línea para que se renderice bien en la tabla
            respuesta_clean = r["respuesta"].replace("\n", "<br>")
            f.write(f"| {r['num']} | **{r['pregunta']}** | {respuesta_clean} | {r['confidence']:.2f} | {r['status']} |\n")
            
    print("Pruebas completadas. Archivo 'resultado_15_preguntas.md' generado.")

if __name__ == "__main__":
    main()
