import os
import re
import threading
import traceback
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")

# Modelo MULTILINGÜE
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Umbral de similitud de distancia coseno (menor = más similar, rango 0 a 2)
# Con coseno, un valor de 0.6 o menor es muy similar.
SIMILARITY_THRESHOLD = 0.65

_vectorstore = None
_lock = threading.Lock()

# Palabras vacías en español que no aportan significado en la búsqueda por keywords
STOP_WORDS = {
    "de", "la", "el", "en", "para", "con", "un", "una", "los", "las", "del", "al", 
    "que", "y", "o", "como", "cual", "cuales", "donde", "dónde", "son", "es", "me", "te",
    "se", "por", "lo", "su", "sus", "para", "mi", "tu", "a", "sobre", "entre"
}

# Mapa de keywords a categorías para fallback / re-ranking
KEYWORD_MAP = {
    "Inscripciones y Admisión": [
        "inscripci", "admisi", "inscribir", "inscribirse", "formulario",
        "cuando abren", "cuándo abren", "fechas de inscripción",
    ],
    "Matrícula y Costos": [
        "matrícula", "matricula", "costo", "precio", "pagar", "cuánto cuesta",
        "matrícula cero", "descuento",
    ],
    "Grados": [
        "grado", "graduarme", "graduación", "graduarse", "ceremonia",
        "requisitos de grado", "título",
    ],
    "Movilidad Internacional": [
        "movilidad", "intercambio", "internacional", "estudiar afuera",
        "convenio", "internacionalización", "pasantía",
    ],
    "Becas y Financiación": [
        "beca", "financiación", "financiamiento", "ayuda económica",
        "apoyo económico",
    ],
    "Oferta Académica": [
        "programa", "carrera", "pregrado", "posgrado", "maestría",
        "doctorado", "ingeniería", "qué puedo estudiar",
    ],
    "Bienestar Universitario": [
        "bienestar", "psicología", "psicólogo", "deporte", "salud",
        "alimentar", "apoyo alimentario",
    ],
    "Reglamento Académico": [
        "reglamento", "norma", "habilitación", "habilitar", "estímulo",
        "calidad de estudiante", "acuerdo 186",
    ],
    "Información General": [
        "ubicación", "ubicada", "dónde queda", "dirección", "contacto",
        "teléfono", "correo", "rector", "historia", "facultad",
    ],
    "Calendario Académico": [
        "calendario", "cuándo empieza", "inicio de clases", "semestre",
        "periodo académico",
    ],
    "Extranjeros": [
        "extranjero", "visa", "foráneo", "otro país", "internacional estudiante",
    ],
}


def _normalizar_texto(texto: str) -> str:
    """Convierte a minúsculas, remueve acentos y caracteres especiales."""
    if not texto:
        return ""
    texto = texto.lower()
    # Reemplazar acentos
    texto = re.sub(r'[áàäâ]', 'a', texto)
    texto = re.sub(r'[éèëê]', 'e', texto)
    texto = re.sub(r'[íìïî]', 'i', texto)
    texto = re.sub(r'[óòöô]', 'o', texto)
    texto = re.sub(r'[úùüû]', 'u', texto)
    # Remover puntuación
    texto = re.sub(r'[^a-z0-9ñ ]', ' ', texto)
    # Normalizar espacios
    return " ".join(texto.split())


def _detectar_categoria(pregunta: str) -> str | None:
    """Detecta la categoría más probable usando keywords simples."""
    pregunta_norm = _normalizar_texto(pregunta)
    best_cat = None
    best_count = 0
    for cat, keywords in KEYWORD_MAP.items():
        count = 0
        for kw in keywords:
            kw_norm = _normalizar_texto(kw)
            if kw_norm in pregunta_norm:
                count += 1
        if count > best_count:
            best_count = count
            best_cat = cat
    return best_cat if best_count > 0 else None


def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        with _lock:
            if _vectorstore is None:
                try:
                    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
                    _vectorstore = Chroma(
                        persist_directory=CHROMA_PERSIST_DIR,
                        embedding_function=embeddings,
                        collection_metadata={"hnsw:space": "cosine"}
                    )
                    count = _vectorstore._collection.count()
                    print(f"[RAG] ChromaDB cargado con {count} documentos (modelo: {EMBEDDING_MODEL}).")
                except Exception as e:
                    print(f"[RAG] Error cargando vectorstore: {e}")
                    traceback.print_exc()
                    return None
    return _vectorstore


def _busqueda_palabras_clave(vs, pregunta: str) -> list:
    """
    Realiza una búsqueda basada en coincidencia de términos textuales (Keyword search)
    sobre todos los documentos cargados en Chroma.
    Retorna una lista de tuplas [(Document, score_hibrido), ...] ordenadas de menor a mayor score.
    """
    # 1. Obtener todos los documentos
    all_data = vs.get()
    ids = all_data.get('ids', [])
    metadatas = all_data.get('metadatas', [])
    documents = all_data.get('documents', [])
    
    # 2. Tokenizar la pregunta del usuario en palabras clave
    pregunta_norm = _normalizar_texto(pregunta)
    palabras_consulta = [w for w in pregunta_norm.split() if w not in STOP_WORDS and len(w) > 2]
    
    if not palabras_consulta:
        # Si no quedan palabras significativas, retornar vacío
        return []
        
    resultados_hibridos = []
    
    # 3. Evaluar coincidencia en cada documento
    for idx in range(len(ids)):
        doc_metadata = metadatas[idx]
        doc_content = documents[idx]
        
        # Obtener campos individuales del documento
        question = _normalizar_texto(doc_metadata.get('question', ''))
        keywords = _normalizar_texto(doc_metadata.get('keywords', ''))
        category = _normalizar_texto(doc_metadata.get('category', ''))
        
        # Calcular coincidencia exacta de palabras
        matches = 0
        for palabra in palabras_consulta:
            # Dar más peso si coincide en la pregunta o en keywords
            if palabra in question:
                matches += 3
            elif palabra in keywords:
                matches += 2
            elif palabra in _normalizar_texto(doc_content):
                matches += 1
                
        if matches > 0:
            # Crear un score virtual: a más coincidencias, menor score (mayor similitud)
            # El score base es 1.0 y se reduce según el número de aciertos.
            score_virtual = max(0.1, 1.0 - (matches * 0.15))
            
            # Crear un objeto de tipo Document de Langchain
            doc_obj = Document(
                page_content=doc_content,
                metadata=doc_metadata
            )
            resultados_hibridos.append((doc_obj, score_virtual))
            
    # Ordenar de menor score (más similar) a mayor
    resultados_hibridos.sort(key=lambda x: x[1])
    return resultados_hibridos


def _formatear_respuesta(docs_con_score: list, categoria_hint: str | None = None) -> dict:
    """
    Recibe [(Document, score), ...] y devuelve la mejor respuesta encontrada.
    Filtra por umbral de similitud para evitar respuestas irrelevantes.
    """
    if not docs_con_score:
        return {
            "result": (
                "No encontré información relacionada a tu consulta en mi base de conocimiento. "
                "Te recomiendo visitar www.unipamplona.edu.co o de manera presencial en nuestras sedes."
            ),
            "source_documents": [],
            "confidence": 0.0,
        }

    # Filtrar solo los documentos con score dentro del umbral
    relevantes = [(doc, score) for doc, score in docs_con_score if score <= SIMILARITY_THRESHOLD]

    # Re-ranking: Si hay un hint de categoría, priorizar la categoría coincidente en el top
    if categoria_hint and relevantes:
        misma_cat = [(d, s) for d, s in relevantes if d.metadata.get("category") == categoria_hint]
        otra_cat = [(d, s) for d, s in relevantes if d.metadata.get("category") != categoria_hint]
        # Si hay de la misma categoría, ponerlos al principio de la lista
        if misma_cat:
            relevantes = misma_cat + otra_cat

    if not relevantes:
        # Hay resultados pero ninguno es suficientemente similar
        return {
            "result": (
                "No tengo información específica sobre eso en mi base de datos. "
                "Para consultas detalladas visita www.unipamplona.edu.co "
                "o comunícate a atencionalciudadano@unipamplona.edu.co."
            ),
            "source_documents": [],
            "confidence": 0.0,
        }

    # Tomar el más relevante (menor score = mayor similitud)
    best_doc, best_score = relevantes[0]
    content = best_doc.page_content

    # Extraer solo la parte de la Respuesta
    if "Respuesta:" in content:
        respuesta = content.split("Respuesta:", 1)[1].strip()
    else:
        respuesta = content.strip()

    # Si hay varios resultados muy relevantes de la misma categoría, combinarlos
    if len(relevantes) > 1:
        categorias_vistas = {best_doc.metadata.get("category", "")}
        extra = []
        for doc, score in relevantes[1:]:
            cat = doc.metadata.get("category", "")
            # Combinar solo si son de diferente pregunta pero misma/diferente categoría con score excelente
            if cat not in categorias_vistas and score < 0.45:
                c = doc.page_content
                if "Respuesta:" in c:
                    extra.append(c.split("Respuesta:", 1)[1].strip())
                categorias_vistas.add(cat)
        if extra:
            respuesta += "\n\n" + "\n\n".join(extra)

    # Calcular confianza normalizada (1 - score/threshold)
    confidence = round(max(0.0, min(1.0, 1 - best_score / SIMILARITY_THRESHOLD)), 2)

    return {
        "result": respuesta,
        "source_documents": [doc for doc, _ in relevantes],
        "confidence": confidence,
    }


def consultar_agente(pregunta: str) -> dict:
    """
    Consulta el agente RAG con la pregunta del usuario.
    Retorna dict con 'result', 'source_documents' y 'confidence'.
    Usa un sistema de búsqueda HÍBRIDO (Semántico + Palabras Clave) para máxima precisión en español.
    """
    try:
        vs = get_vectorstore()
        if vs is None:
            return {
                "result": "Error al conectar con la base de conocimiento. Por favor intenta de nuevo.",
                "source_documents": [],
                "confidence": 0.0,
            }

        # 1. Detectar categoría a partir de keywords de la consulta (hint para re-ranking)
        categoria_hint = _detectar_categoria(pregunta)

        # 2. Búsqueda por palabras clave (coincidencia de términos)
        docs_keywords = _busqueda_palabras_clave(vs, pregunta)

        # 3. Búsqueda semántica clásica (distancia coseno de embeddings)
        docs_semanticos = vs.similarity_search_with_score(pregunta, k=5)

        # 4. Fusionar y desduplicar resultados
        # Damos prioridad a los matches por palabra clave si son fuertes (score virtual bajo)
        fusionados = []
        preguntas_vistas = set()

        print(f"[RAG] Pregunta: '{pregunta}' | Hint Categoría: {categoria_hint}")

        # Primero agregamos los de coincidencia de palabras clave si tienen buen score (< 0.8)
        for doc, score in docs_keywords:
            q = doc.metadata.get("question")
            if q not in preguntas_vistas:
                preguntas_vistas.add(q)
                fusionados.append((doc, score))
                print(f"  [KEYWORD] score={score:.4f} | cat={doc.metadata.get('category')} | {q[:70]}")

        # Luego agregamos los semánticos que no estén ya agregados
        for doc, score in docs_semanticos:
            q = doc.metadata.get("question")
            if q not in preguntas_vistas:
                preguntas_vistas.add(q)
                fusionados.append((doc, score))
                print(f"  [SEMANTIC] score={score:.4f} | cat={doc.metadata.get('category')} | {q[:70]}")

        # Ordenar todo de nuevo por score
        fusionados.sort(key=lambda x: x[1])

        return _formatear_respuesta(fusionados, categoria_hint)

    except Exception as e:
        print(f"[RAG] Error en consultar_agente: {e}")
        traceback.print_exc()
        return {
            "result": "Ocurrió un error interno al procesar tu consulta. Por favor intenta de nuevo.",
            "source_documents": [],
            "confidence": 0.0,
        }
