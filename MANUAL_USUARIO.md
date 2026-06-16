# 📘 Manual de Usuario
# Asistente de Orientación Académica — Universidad de Pamplona

**Versión:** 1.0  
**Fecha:** Junio 2026  
**Tecnologías:** FastAPI · React · LangChain · ChromaDB · SQLite

---

## Tabla de Contenidos

1. [Descripción General](#1-descripción-general)
2. [Arquitectura del Sistema](#2-arquitectura-del-sistema)
3. [Requisitos Previos](#3-requisitos-previos)
4. [Instalación del Backend](#4-instalación-del-backend)
5. [Instalación del Frontend](#5-instalación-del-frontend)
6. [Configuración de Variables de Entorno](#6-configuración-de-variables-de-entorno)
7. [Uso de la Aplicación (Usuario Final)](#7-uso-de-la-aplicación-usuario-final)
8. [Panel Administrativo](#8-panel-administrativo)
9. [Pipeline de Entrenamiento](#9-pipeline-de-entrenamiento)
10. [Suite de Pruebas](#10-suite-de-pruebas)
11. [Referencia de la API REST](#11-referencia-de-la-api-rest)
12. [Solución de Problemas Frecuentes](#12-solución-de-problemas-frecuentes)

---

## 1. Descripción General

El **Asistente de Orientación Académica** es un chatbot inteligente basado en técnica **RAG** *(Retrieval-Augmented Generation)* diseñado para responder preguntas frecuentes de estudiantes y aspirantes a la Universidad de Pamplona (Colombia).

### Funcionalidades principales

| Función | Descripción |
|---|---|
| 💬 Chat inteligente | Responde preguntas sobre inscripciones, grados, matrícula, etc. |
| 📚 Base de conocimiento | Indexa documentos y FAQs en una base vectorial ChromaDB |
| 🔍 Búsqueda semántica | Recupera el fragmento más relevante para cada pregunta |
| 🛠️ Panel Admin | Gestión de categorías, FAQs, métricas y logs |
| 🔄 Reentrenamiento | Pipeline para actualizar el modelo desde la base de datos |
| 🗄️ Historial | Persistencia de conversaciones en SQLite |

---

## 2. Arquitectura del Sistema

```
chatbot/
├── backend/                   # API FastAPI (Python)
│   ├── main.py                # Servidor principal y endpoints
│   ├── rag_agent.py           # Motor de búsqueda RAG (ChromaDB)
│   ├── training_pipeline.py   # Pipeline de entrenamiento / indexación
│   ├── models.py              # Modelos de base de datos (SQLAlchemy)
│   ├── database.py            # Conexión SQLite
│   ├── seed_data.py           # Datos iniciales de conocimiento
│   ├── run_tests.py           # Suite de pruebas de integración
│   ├── test_agent.py          # Prueba directa del agente RAG
│   ├── requirements.txt       # Dependencias Python
│   ├── chatbot.db             # Base de datos SQLite (auto-generada)
│   ├── chroma_db_unipamplona/ # Índice vectorial (auto-generado)
│   └── docs/
│       └── guia_texto.txt     # Documento fuente de conocimiento
│
├── src/                       # Frontend React + TypeScript
│   ├── App.tsx                # Componente raíz con routing hash
│   ├── sections/
│   │   ├── Hero.tsx           # Sección de bienvenida
│   │   ├── ChatSection.tsx    # Interfaz principal del chat
│   │   ├── Categories.tsx     # Categorías de preguntas
│   │   ├── FAQ.tsx            # Preguntas frecuentes
│   │   ├── Contact.tsx        # Información de contacto
│   │   └── AdminPanel.tsx     # Panel de administración
│   ├── services/api.ts        # Cliente HTTP hacia el backend
│   ├── stores/                # Estado global (Zustand)
│   └── types/                 # Tipos TypeScript
│
├── .env                       # Variables de entorno (no subir a Git)
├── .env.example               # Plantilla de variables de entorno
└── package.json               # Dependencias y scripts del frontend
```

### Flujo de una consulta

```
Usuario escribe pregunta
        │
        ▼
 Frontend (React) ──POST /api/chat/message──► Backend (FastAPI)
                                                     │
                                            Guarda mensaje en SQLite
                                                     │
                                            ChromaDB similarity_search(k=1)
                                                     │
                                            Extrae fragmento más relevante
                                                     │
                                            Guarda respuesta en SQLite
                                                     │
        Frontend ◄──── JSON ChatResponse ────  Retorna respuesta
```

---

## 3. Requisitos Previos

### Software requerido

| Herramienta | Versión mínima | Verificación |
|---|---|---|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | cualquiera | `git --version` |

### Hardware recomendado

- **RAM:** mínimo 4 GB (8 GB recomendados para embeddings)
- **Disco:** mínimo 2 GB libres (para modelos HuggingFace)
- **CPU:** cualquier procesador moderno (no requiere GPU)

> [!NOTE]
> El modelo de embeddings `all-MiniLM-L6-v2` se descarga automáticamente (~90 MB) la primera vez que se inicia el backend.

---

## 4. Instalación del Backend

### Paso 1 — Ubicarse en el directorio backend

```powershell
cd C:\Users\Asly Acuña\Documents\chatbot\backend
```

### Paso 2 — Crear entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> [!TIP]
> Si PowerShell bloquea la ejecución de scripts, ejecuta primero:  
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### Paso 3 — Instalar dependencias

```powershell
pip install -r requirements.txt
```

Las principales dependencias instaladas son:

| Paquete | Función |
|---|---|
| `fastapi` + `uvicorn` | Servidor web asíncrono |
| `sqlalchemy` | ORM para SQLite |
| `langchain` + `langchain-community` | Framework RAG |
| `langchain-huggingface` | Embeddings con HuggingFace |
| `chromadb` | Base de datos vectorial |
| `sentence-transformers` | Modelo `all-MiniLM-L6-v2` |
| `pypdf` | Lectura de documentos PDF |

### Paso 4 — Poblar la base de datos inicial

```powershell
python seed_data.py
```

Esto crea el archivo `chatbot.db` e inserta:
- **5 entradas de conocimiento** (Inscripciones, Grados, Extranjeros, Matrícula, General)
- **3 intenciones** (saludo, requisitos_grado, inscripcion)

### Paso 5 — Ejecutar el pipeline de entrenamiento (indexación vectorial)

```powershell
python training_pipeline.py
```

Esto genera la carpeta `chroma_db_unipamplona/` con los vectores del conocimiento.

### Paso 6 — Iniciar el servidor

```powershell
uvicorn main:app --reload --port 8001
```

El backend estará disponible en: **http://127.0.0.1:8001**

Verifica que funciona abriendo en el navegador:
```
http://127.0.0.1:8001/
```
Respuesta esperada:
```json
{"status": "ok", "message": "API RAG corriendo exitosamente."}
```

La documentación interactiva Swagger estará en: `http://127.0.0.1:8001/docs`

---

## 5. Instalación del Frontend

### Paso 1 — Ir a la raíz del proyecto

```powershell
cd C:\Users\Asly Acuña\Documents\chatbot
```

### Paso 2 — Instalar dependencias Node

```powershell
npm install
```

Dependencias principales del frontend:

| Paquete | Función |
|---|---|
| `react` 19 | Librería de interfaz |
| `vite` | Bundler y servidor de desarrollo |
| `framer-motion` | Animaciones fluidas |
| `zustand` | Gestión de estado global |
| `@tanstack/react-query` | Cache y sincronización de datos |
| `uuid` | Generación de IDs de sesión únicos |

### Paso 3 — Configurar variables de entorno

```powershell
copy .env.example .env
```

Edita el archivo `.env` con tus valores (ver sección 6).

### Paso 4 — Iniciar el servidor de desarrollo

```powershell
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

---

## 6. Configuración de Variables de Entorno

### Archivo `.env` (raíz del proyecto)

| Variable | Descripción | Ejemplo |
|---|---|---|
| `VITE_API_URL` | URL base de la API del backend | `http://localhost:8001/api` |
| `VITE_ADMIN_ACCESS_CODE` | Código para acceder al panel admin | `mi-clave-secreta` |

> [!WARNING]
> **Nunca** subas el archivo `.env` al repositorio. Ya está incluido en `.gitignore`.

---

## 7. Uso de la Aplicación (Usuario Final)

### 7.1 Página principal

Al ingresar a `http://localhost:5173` el usuario verá las siguientes secciones:

| Sección | Descripción |
|---|---|
| **Hero** | Presentación del asistente con botón de inicio |
| **Chat** | Interfaz principal de conversación |
| **Categorías** | Acceso rápido por tema (Inscripciones, Grados…) |
| **FAQ** | Preguntas frecuentes expandibles |
| **Contacto** | Información de contacto de la Universidad |

### 7.2 Usar el chat

1. Haz clic en la sección **Chat** o en el botón principal del Hero.
2. Escribe tu pregunta en el campo de texto, por ejemplo:
   - *"¿Cuáles son los requisitos de grado?"*
   - *"¿Cómo me inscribo en la universidad?"*
   - *"¿Cuándo son las fechas de matrícula?"*
3. Presiona **Enter** o el botón de enviar.
4. El asistente responderá en segundos con la información más relevante.

### 7.3 Comportamiento del chat

- Cada sesión genera un **ID único (UUID)** automáticamente al abrir la página.
- El historial de conversación se **persiste en la base de datos SQLite**.
- Si el asistente no encuentra información dice: *"No encontré información relacionada a tu pregunta."*
- El nivel de confianza: **0.9** si encontró documentos fuente, **0.5** si no.

### 7.4 Temas disponibles

| Categoría | Preguntas cubiertas (ejemplos) |
|---|---|
| 📝 Inscripciones | Proceso de inscripción, requisitos, plazos, pago del pin |
| 🎓 Grados | Requisitos de graduación, trabajo de grado, paz y salvo |
| 🌍 Extranjeros | Documentos requeridos, visa de estudiante, convalidación |
| 💳 Matrícula | Fechas de pago, montos, procedimientos |
| 📍 General | Ubicación, sedes, información institucional |

---

## 8. Panel Administrativo

### 8.1 Acceder al panel

Navega a:
```
http://localhost:5173/#admin
```

### 8.2 Proceso de autenticación (dos etapas)

**Etapa 1 — Código de acceso**
1. Ingresa el valor de `VITE_ADMIN_ACCESS_CODE` definido en tu `.env`.
2. Haz clic en **"Validar acceso"**.

**Etapa 2 — Login administrativo**
1. Ingresa las credenciales:
   - **Email:** `admin@unipamplona.edu.co`
   - **Contraseña:** `admin123`
2. Haz clic en **"Ingresar"**.

> [!CAUTION]
> Cambia las credenciales por defecto antes de desplegar en producción.

### 8.3 Dashboard de métricas

Una vez autenticado verás tarjetas con:

| Métrica | Descripción |
|---|---|
| **Categorías** | Total de categorías registradas |
| **FAQs** | Total de preguntas frecuentes activas |
| **Conversaciones** | Total de sesiones de chat iniciadas |
| **Mensajes** | Total de mensajes intercambiados |

### 8.4 Gestión de Categorías

Desde el panel izquierdo puedes:
- **Crear** una nueva categoría llenando: `Slug`, `Nombre`, `Descripción`, `Icono` (emoji).
- **Editar** una categoría existente haciendo clic en "Editar".
- **Eliminar** una categoría.
- **Seleccionar** una categoría para ver/editar sus FAQs.

**Campos del formulario de categoría:**

| Campo | Descripción | Ejemplo |
|---|---|---|
| Slug | Identificador único en minúsculas | `inscripciones` |
| Nombre | Nombre visible en la interfaz | `Inscripciones` |
| Descripción | Descripción corta | `Proceso de admisión` |
| Icono | Emoji representativo | `📝` |

### 8.5 Gestión de FAQs

Desde el panel derecho (seleccionando una categoría):
- **Crear** una nueva FAQ con pregunta, respuesta, keywords y temas relacionados.
- **Editar** una FAQ existente.
- **Eliminar** una FAQ.

**Campos del formulario de FAQ:**

| Campo | Descripción | Ejemplo |
|---|---|---|
| Pregunta | Pregunta en lenguaje natural | `¿Cómo me inscribo?` |
| Respuesta | Respuesta detallada | `Para inscribirte debes...` |
| Keywords | Palabras clave separadas por coma | `inscripción, admisión` |
| Related topics | Temas relacionados separados por coma | `matrícula, documentos` |

### 8.6 Logs recientes

La sección inferior muestra los últimos registros de actividad con:
- Método HTTP y URL consultada
- Código de estado de respuesta
- Tiempo de respuesta en milisegundos

### 8.7 Cerrar sesión

Haz clic en **"Cerrar sesión"** en la barra superior del panel.

---

## 9. Pipeline de Entrenamiento

El pipeline convierte el conocimiento de la base de datos en vectores semánticos que el agente RAG utiliza para encontrar respuestas.

### 9.1 Cuándo reentrenar

Debes ejecutar el pipeline cuando:
- Agregues o edites FAQs desde el panel admin.
- Modifiques el archivo `docs/guia_texto.txt`.
- La calidad de las respuestas del chatbot disminuya.

### 9.2 Ejecución manual

```powershell
cd backend
python training_pipeline.py
```

Salida esperada:
```
{'status': 'success', 'chunks': 45, 'docs': 10}
```

### 9.3 Ejecución desde la API

```
POST http://127.0.0.1:8001/api/admin/train
```

### 9.4 Pasos internos del pipeline

| Paso | Descripción |
|---|---|
| 1. Recuperar conocimiento | Lee todos los registros activos de la tabla `conocimiento` |
| 2. Cargar guía de texto | Carga `docs/guia_texto.txt` si existe |
| 3. Limpieza | Normaliza espacios y saltos de línea |
| 4. Splitting | Divide documentos en chunks de 500 caracteres (overlap 100) |
| 5. Embeddings | Genera vectores con `all-MiniLM-L6-v2` |
| 6. Almacenamiento | Persiste vectores en `chroma_db_unipamplona/` |

### 9.5 Agregar documentos de conocimiento

Coloca archivos `.txt` en `backend/docs/` con el formato:

```
Pregunta: ¿Cuál es el horario de la biblioteca?
Respuesta: La biblioteca está disponible de lunes a viernes de 7am a 9pm.
```

Luego ejecuta el pipeline de entrenamiento para indexar el nuevo contenido.

---

## 10. Suite de Pruebas

### 10.1 Requisitos

El backend debe estar corriendo en `http://127.0.0.1:8001` antes de ejecutar las pruebas.

### 10.2 Ejecutar todas las pruebas

```powershell
cd backend
python run_tests.py
```

### 10.3 Descripción de cada prueba

| # | Nombre | Qué verifica |
|---|---|---|
| 1 | Conexión Backend ↔ Base de Datos | `/api/admin/metrics` responde HTTP 200 con JSON válido |
| 2 | Creación y almacenamiento de conversación | Nueva sesión persiste 2 mensajes (usuario + bot) |
| 3 | Consulta del conocimiento entrenado | `/api/categories/grados/faqs` retorna resultados |
| 4 | Respuesta contextual del chatbot | Respuesta sobre "requisitos de grado" menciona "créditos" |
| 5 | Carga simultánea (5 usuarios) | 5 consultas concurrentes retornan todas HTTP 200 |

### 10.4 Interpretar resultados

```
==================================================
TEST: 2. Creación y almacenamiento de conversación
STATUS: PASSED
EXPECTED: Conversation created with 2 messages
OBTAINED: Messages found: 2
==================================================
```

- `STATUS: PASSED` ✅ — La prueba fue exitosa.
- `STATUS: FAILED` ❌ — Revisa el campo `OBTAINED` para identificar el error.

### 10.5 Prueba directa del agente RAG

```powershell
python test_agent.py
```

Prueba el módulo `rag_agent.py` directamente sin pasar por la API HTTP.

---

## 11. Referencia de la API REST

**Base URL:** `http://127.0.0.1:8001`  
**Documentación interactiva (Swagger):** `http://127.0.0.1:8001/docs`

### Endpoints de Chat

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/chat/message` | Envía mensaje y obtiene respuesta del asistente |
| `GET` | `/api/chat/history/{sessionId}` | Recupera historial de una sesión |
| `DELETE` | `/api/chat/history/{sessionId}` | Elimina historial de una sesión |

**POST `/api/chat/message` — Request:**
```json
{
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "message": "¿Cuáles son los requisitos de grado?",
  "category": "grados"
}
```

**POST `/api/chat/message` — Response:**
```json
{
  "id": "42",
  "response": "Los requisitos principales son: 1. Haber aprobado todos los créditos...",
  "category": "grados",
  "confidence": 0.9,
  "relatedTopics": ["Guía de Orientación Académica"],
  "timestamp": "2026-06-16T15:30:00Z"
}
```

### Endpoints de Categorías

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/categories` | Lista todas las categorías |
| `GET` | `/api/categories/{slug}/faqs` | FAQs de una categoría por slug |

### Endpoints Administrativos

| Método | Endpoint | Descripción |
|---|---|---|
| `POST` | `/api/auth/login` | Autenticación de administrador |
| `GET` | `/api/admin/metrics` | Métricas generales del sistema |
| `GET` | `/api/admin/logs?limit=20` | Logs de actividad recientes |
| `POST` | `/api/admin/train` | Dispara el pipeline de reentrenamiento |

---

## 12. Solución de Problemas Frecuentes

### ❌ `ModuleNotFoundError` al iniciar el backend

**Causa:** Las dependencias de Python no están instaladas en el entorno activo.

**Solución:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### ❌ El chat responde "No encontré información relacionada"

**Causa:** La base vectorial ChromaDB no ha sido generada o está vacía.

**Solución:**
1. Ejecuta `python seed_data.py` para poblar la BD.
2. Ejecuta `python training_pipeline.py` para indexar.
3. Reinicia el servidor `uvicorn`.

---

### ❌ Error CORS en el frontend

**Causa:** La URL del backend en `.env` no coincide con el puerto real del servidor.

**Solución:**
- Verifica que `VITE_API_URL=http://localhost:8001/api` en tu `.env`.
- Asegúrate de que uvicorn corre en el puerto `8001`.
- Reinicia Vite (`npm run dev`) después de editar `.env`.

---

### ❌ Panel admin muestra "Código de acceso inválido"

**Causa:** `VITE_ADMIN_ACCESS_CODE` en `.env` no coincide con el valor ingresado.

**Solución:**
- Revisa el valor exacto en tu archivo `.env`.
- El campo es sensible a mayúsculas/minúsculas.
- Reinicia Vite si acabas de editar el `.env`.

---

### ❌ Modelo de embeddings no descarga

**Causa:** Sin conexión a internet en el primer arranque.

**Solución:**
- Asegura conexión a internet la primera vez.
- El modelo `all-MiniLM-L6-v2` (~90 MB) se descarga desde HuggingFace Hub y se cachea en `~/.cache/huggingface/`.

---

### ❌ Puerto 8001 ya está en uso

**Solución:**
```powershell
# Buscar proceso usando el puerto
netstat -ano | findstr :8001

# Terminar proceso (reemplaza PID con el número encontrado)
taskkill /PID <PID> /F
```
O usar un puerto alternativo:
```powershell
uvicorn main:app --reload --port 8002
```
Y actualizar `VITE_API_URL=http://localhost:8002/api` en `.env`.

---

## Glosario

| Término | Definición |
|---|---|
| **RAG** | Retrieval-Augmented Generation: búsqueda semántica + generación de texto |
| **ChromaDB** | Base de datos vectorial para búsqueda por similitud semántica |
| **Embedding** | Representación numérica de texto que captura su significado |
| **Chunk** | Fragmento en que se dividen los documentos para indexación |
| **FastAPI** | Framework web Python de alto rendimiento para APIs REST |
| **SQLite** | Base de datos relacional ligera almacenada en `chatbot.db` |
| **Vite** | Herramienta de build ultrarrápida para proyectos frontend |
| **Zustand** | Librería minimalista de estado global para React |
| **sessionId** | UUID único que agrupa los mensajes de una conversación |

---

*Manual generado para el proyecto Asistente de Orientación Académica — Universidad de Pamplona, Colombia.*
