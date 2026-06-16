import sys
import os

# Agregamos la ruta del directorio actual para importar los módulos correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_agent import consultar_agente

def main():
    print("="*60)
    print("PRUEBA DE ENTRENAMIENTO Y CONSULTA DEL AGENTE RAG")
    print("="*60)
    
    # Al llamar a consultar_agente por primera vez, el sistema:
    # 1. Verifica si existe ChromaDB
    # 2. Si no, carga el PDF "Guia_Orientacion_Academica_Unipamplona.pdf"
    # 3. Lo divide en fragmentos (chunks)
    # 4. Genera embeddings usando sentence-transformers
    # 5. Guarda la base vectorial en la carpeta chroma_db_unipamplona
    
    pregunta = "¿Cuáles son los requisitos para estudiantes extranjeros?"
    print(f"\nRealizando consulta de prueba: '{pregunta}'\n")
    
    try:
        resultado = consultar_agente(pregunta)
        
        print("\n--- RESPUESTA GENERADA ---")
        print(resultado.get("result", "Sin respuesta"))
        
        print("\n--- FRAGMENTOS RECUPERADOS DE LA BASE DE DATOS ---")
        docs = resultado.get("source_documents", [])
        for i, doc in enumerate(docs):
            print(f"\nFragmento {i+1}:")
            print(doc.page_content[:200] + "...")
            
        print("\nPrueba finalizada con éxito. La base de datos vectorial ha sido inicializada y probada.")
    except Exception as e:
        print(f"Error durante la prueba: {e}")

if __name__ == "__main__":
    main()
