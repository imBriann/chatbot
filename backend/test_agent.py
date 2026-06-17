import sys
import os

# Agregamos la ruta del directorio actual para importar los módulos correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_agent import consultar_agente

# Configurar stdout para evitar problemas con UTF-8 en Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def probar_pregunta(pregunta):
    print("\n" + "="*80)
    print(f"PREGUNTA: {pregunta}")
    print("="*80)
    res = consultar_agente(pregunta)
    print(f"CONFIANZA: {res.get('confidence')}")
    print(f"RESPUESTA:\n{res.get('result')}")
    print("-" * 80)
    docs = res.get("source_documents", [])
    print(f"FUENTES DETECTADAS ({len(docs)}):")
    for i, doc in enumerate(docs[:3]):
        q = doc.metadata.get("question", "Sin pregunta")
        cat = doc.metadata.get("category", "Sin categoria")
        print(f"  {i+1}. [{cat}] {q}")

def main():
    preguntas = [
        "cuando son las inscripciones",
        "inscripciones",
        "movilidad academica",
        "movilidad",
        "cuales son los requisitos de inscripcion",
        "donde queda la universidad",
        "bienestar universitario",
        "becas",
    ]
    for q in preguntas:
        probar_pregunta(q)

if __name__ == "__main__":
    main()
