import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    print(f"Total documentos en ChromaDB: {vs._collection.count()}")
    
    query = "becas"
    print(f"\nBuscando: '{query}'")
    results = vs.similarity_search_with_score(query, k=10)
    for i, (doc, score) in enumerate(results):
        print(f"\n--- Resultado {i+1} (Score: {score:.4f}) ---")
        print(f"Pregunta: {doc.metadata.get('question')}")
        print(f"Categoria: {doc.metadata.get('category')}")
        print(f"Content snippet: {doc.page_content[:150]}...")

if __name__ == "__main__":
    main()
