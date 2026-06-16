import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from transformers import pipeline
import traceback
import threading

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")

prompt_template = """Eres un asistente virtual especializado en orientacion academica de la Universidad de Pamplona (Colombia). Tu mision es brindar informacion clara, precisa y util. Te presentas siempre como: "Asistente de Orientacion Academica de la Universidad de Pamplona".

Contexto recuperado:
{context}

Pregunta: {question}

Respuesta:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

vectorstore = None
hf_pipeline = None
vectorstore_lock = threading.Lock()

def get_vectorstore():
    global vectorstore
    if vectorstore is None:
        with vectorstore_lock:
            if vectorstore is None:
                try:
                    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                    vectorstore = Chroma(persist_directory=CHROMA_PERSIST_DIR, embedding_function=embeddings)
                except Exception as e:
                    print(f"Error cargando vectorstore: {str(e)}")
                    traceback.print_exc()
                    return None
    return vectorstore

def get_pipeline():
    def mock_pipeline(prompt):
        start_idx = prompt.find("Contexto recuperado:\n") + len("Contexto recuperado:\n")
        end_idx = prompt.find("\n\nPregunta:")
        context = prompt[start_idx:end_idx].strip()
        if not context:
            return [{'generated_text': 'No tengo información sobre eso.'}]
        return [{'generated_text': context}]
    return mock_pipeline

def consultar_agente(pregunta: str, timeout: int = 30):
    try:
        vs = get_vectorstore()
        if vs is None:
            return {
                "result": "Error al conectar con la base de datos. Por favor intenta de nuevo.",
                "source_documents": []
            }
        
        # Solo necesitamos el documento más relevante para no saturar al usuario
        try:
            docs = vs.similarity_search(pregunta, k=1)
        except Exception as e:
            print(f"Error en similarity_search: {str(e)}")
            traceback.print_exc()
            return {
                "result": "No encontré información relacionada a tu pregunta. Por favor intenta con otra consulta.",
                "source_documents": []
            }
        
        if not docs:
            return {
                "result": "No encontré información relacionada a tu pregunta. ¿Podrías reformular tu consulta?",
                "source_documents": []
            }
            
        # El documento tiene formato "Pregunta: ... \nRespuesta: ..."
        best_doc = docs[0].page_content
        answer = best_doc
        
        if "Respuesta:" in best_doc:
            answer = best_doc.split("Respuesta:", 1)[1].strip()
            
        return {
            "result": answer,
            "source_documents": docs
        }
    except Exception as e:
        print(f"Error en consultar_agente: {str(e)}")
        traceback.print_exc()
        return {
            "result": "Hubo un error al procesar tu solicitud. Por favor intenta de nuevo más tarde.",
            "source_documents": []
        }
