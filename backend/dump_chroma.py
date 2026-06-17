import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def main():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    print("Listando todos los documentos guardados en ChromaDB:")
    # Get all documents
    data = vs.get()
    ids = data.get('ids', [])
    metadatas = data.get('metadatas', [])
    documents = data.get('documents', [])
    
    print(f"Total encontrados: {len(ids)}")
    for i in range(len(ids)):
        print(f"\nID: {ids[i]}")
        print(f"Metadata: {metadatas[i]}")
        print(f"Content: {repr(documents[i][:200])}...")

if __name__ == "__main__":
    main()
