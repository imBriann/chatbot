import requests
import json
import uuid
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://127.0.0.1:8001/api"

def print_test(name, passed, expected, obtained, log=""):
    status = "PASSED" if passed else "FAILED"
    print(f"\n{'='*50}\nTEST: {name}\nSTATUS: {status}")
    print(f"EXPECTED: {expected}\nOBTAINED: {obtained}")
    if log:
        print(f"LOGS:\n{log}")
    print('='*50)

def test_1_db_connection():
    try:
        resp = requests.get(f"{BASE_URL}/admin/metrics")
        data = resp.json()
        passed = resp.status_code == 200 and 'metrics' in data
        print_test("1. Conexión Backend <-> Base de Datos", passed, "HTTP 200, metrics JSON", f"HTTP {resp.status_code}, {data}")
    except Exception as e:
        print_test("1. Conexión Backend <-> Base de Datos", False, "HTTP 200, metrics JSON", str(e))

def test_2_conversation_creation():
    session_id = str(uuid.uuid4())
    try:
        resp = requests.post(f"{BASE_URL}/chat/message", json={
            "sessionId": session_id,
            "message": "Hola, esto es una prueba."
        })
        data = resp.json()
        
        hist_resp = requests.get(f"{BASE_URL}/chat/history/{session_id}")
        hist_data = hist_resp.json()
        
        passed = resp.status_code == 200 and len(hist_data.get('messages', [])) == 2
        print_test("2. Creación y almacenamiento de conversación", passed, "Conversation created with 2 messages", f"Messages found: {len(hist_data.get('messages', []))}", json.dumps(hist_data, indent=2))
    except Exception as e:
        print_test("2. Creación y almacenamiento de conversación", False, "Conversation created", str(e))

def test_3_knowledge_query():
    try:
        resp = requests.get(f"{BASE_URL}/categories/grados/faqs")
        data = resp.json()
        passed = resp.status_code == 200 and len(data.get('faqs', [])) > 0
        print_test("3. Consulta del conocimiento entrenado", passed, "Returns FAQs for grados", f"Found {len(data.get('faqs', []))} FAQs", json.dumps(data, indent=2))
    except Exception as e:
        print_test("3. Consulta del conocimiento entrenado", False, "Returns FAQs", str(e))

def test_4_contextual_response():
    session_id = str(uuid.uuid4())
    try:
        resp = requests.post(f"{BASE_URL}/chat/message", json={
            "sessionId": session_id,
            "message": "¿Cuáles son los requisitos de grado?"
        })
        data = resp.json()
        passed = resp.status_code == 200 and "créditos" in data.get('response', '').lower()
        print_test("4. Respuesta contextual del chatbot", passed, "Respuesta menciona créditos o requisitos", data.get('response'), json.dumps(data, indent=2))
    except Exception as e:
        print_test("4. Respuesta contextual del chatbot", False, "Respuesta correcta", str(e))

def test_5_concurrent_queries():
    def make_query(i):
        return requests.post(f"{BASE_URL}/chat/message", json={"sessionId": str(uuid.uuid4()), "message": f"Hola {i}"}).status_code
    
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(make_query, range(5)))
        passed = all(code == 200 for code in results)
        print_test("5. Carga simultánea de múltiples consultas", passed, "All 5 queries return 200", f"Status codes: {results}")
    except Exception as e:
        print_test("5. Carga simultánea de múltiples consultas", False, "All 200", str(e))

if __name__ == "__main__":
    test_1_db_connection()
    test_2_conversation_creation()
    test_3_knowledge_query()
    test_4_contextual_response()
    test_5_concurrent_queries()
