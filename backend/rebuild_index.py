"""
Reconstruye el índice ChromaDB desde la base de conocimiento.
Usa modelo MULTILINGÜE para correcto matching en español.
Ejecutar: python rebuild_index.py
"""
import os
import sys
import shutil

# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")

# Modelo MULTILINGÜE — entiende español nativo, mucho mejor que all-MiniLM-L6-v2
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# ── Base de conocimiento con keywords para mejor matching ─────────────────────
SECTIONS = [
    {
        "category": "Información General",
        "chunks": [
            {
                "question": "¿Dónde está ubicada la Universidad de Pamplona?",
                "keywords": "ubicación dirección sede campus dónde queda lugar",
                "answer": (
                    "La sede principal está en Pamplona, Norte de Santander (Km 1 Vía Bucaramanga, Ciudad Universitaria). "
                    "También tiene sede en Villa del Rosario (Autopista Internacional Vía Los Álamos, Villa Antigua) y en Cúcuta."
                ),
            },
            {
                "question": "¿Cómo me puedo contactar con la Universidad de Pamplona?",
                "keywords": "contacto teléfono correo email horario atención",
                "answer": (
                    "Teléfonos: (+57) 315 3429495 – (+57) 316 0244475. "
                    "Correos: atencionalciudadano@unipamplona.edu.co · villarosario@unipamplona.edu.co. "
                    "Horario: lunes a viernes de 8:00 a.m. a 12:00 m. y de 2:00 p.m. a 6:00 p.m. "
                    "Sitio web: www.unipamplona.edu.co"
                ),
            },
            {
                "question": "¿Cuál es la historia de la Universidad de Pamplona?",
                "keywords": "historia fundación origen creación cuando se fundó",
                "answer": (
                    "La Universidad de Pamplona nació en 1960 como institución privada bajo el liderazgo del presbítero "
                    "José Rafael Faría Bermúdez. Posteriormente se consolidó como universidad pública departamental, "
                    "acreditada en Alta Calidad, con sedes en Pamplona, Villa del Rosario y Cúcuta."
                ),
            },
            {
                "question": "¿Cuántas facultades tiene la Universidad de Pamplona y cuáles son?",
                "keywords": "facultades carreras áreas departamentos",
                "answer": (
                    "La Universidad cuenta con 7 facultades: Artes y Humanidades, Ciencias Agrarias, Ciencias Básicas, "
                    "Ciencias Económicas y Empresariales, Ciencias de la Educación, Ingenierías y Arquitectura, y Salud."
                ),
            },
            {
                "question": "¿Quién es el rector de la Universidad de Pamplona?",
                "keywords": "rector director autoridad máxima quien dirige",
                "answer": "El rector es el Dr. Ivaldo Torres Chávez, con periodo 2025–2028.",
            },
        ],
    },
    {
        "category": "Oferta Académica",
        "chunks": [
            {
                "question": "¿Cuántos programas de pregrado ofrece la Universidad de Pamplona?",
                "keywords": "programas pregrado carreras oferta académica qué puedo estudiar",
                "answer": (
                    "La Universidad ofrece 43 programas de pregrado, de los cuales 12 cuentan con Acreditación en Alta Calidad. "
                    "Se distribuyen en modalidad presencial (Pamplona y Villa del Rosario–Cúcuta), a distancia e híbrida. "
                    "Entre ellos: Arquitectura, Diseño Industrial, Ingeniería Civil, Medicina, Derecho y Psicología."
                ),
            },
            {
                "question": "¿Qué programas de posgrado ofrece Unipamplona?",
                "keywords": "posgrado maestría doctorado especialización",
                "answer": (
                    "La Universidad ofrece 15 maestrías, 8 especializaciones y 3 doctorados consolidados. "
                    "Hay nuevos programas doctorales en proceso en: Actividad Física y Deporte, Arte y Cultura, "
                    "Ciencias Agrarias, Ciencias de la Educación, Fonoaudiología, Humanidades y Salud Pública."
                ),
            },
            {
                "question": "¿Qué programas ofrece la Facultad de Ingenierías?",
                "keywords": "ingeniería arquitectura diseño industrial programas ingenierías",
                "answer": (
                    "La Facultad de Ingenierías y Arquitectura ofrece programas como Ingeniería Civil, Arquitectura "
                    "y Diseño Industrial, entre otros, en modalidad presencial en Pamplona y Villa del Rosario–Cúcuta."
                ),
            },
            {
                "question": "¿Hay programas a distancia en Unipamplona?",
                "keywords": "distancia virtual online remoto no presencial",
                "answer": (
                    "Sí, la universidad ofrece programas en modalidad a distancia. Entre los más destacados están "
                    "Administración de Empresas y Contaduría Pública."
                ),
            },
        ],
    },
    {
        "category": "Inscripciones y Admisión",
        "chunks": [
            {
                "question": "¿Cuáles son los requisitos de inscripción o admisión a Unipamplona?",
                "keywords": "requisitos inscripción admisión documentos necesarios papeleo formulario",
                "answer": (
                    "Los requisitos generales son: diligenciar el formulario de inscripción en línea, subir fotografía "
                    "reciente (fondo azul, tamaño 3x4), ser bachiller graduado con diploma o acta de grado, haber presentado "
                    "las Pruebas Saber 11, presentar documento de identidad y recibo de servicios públicos del lugar de residencia."
                ),
            },
            {
                "question": "¿Cuándo son las inscripciones en Unipamplona?",
                "keywords": "cuándo inscripciones fechas periodo plazo abren cierran calendario inscripción",
                "answer": (
                    "Las fechas de inscripción se aprueban semestralmente mediante acuerdo del Consejo Académico. "
                    "Para el segundo periodo de 2026 rigen los Acuerdos N.° 021 y 022 del 21 de abril de 2026. "
                    "Consulta las fechas vigentes en: unipamplona.edu.co/registroycontrol → Calendarios Académicos Vigentes."
                ),
            },
            {
                "question": "¿Cuáles son las modalidades de ingreso a la universidad?",
                "keywords": "modalidades ingreso formas entrar tipos admisión transferencia reingreso",
                "answer": (
                    "Las modalidades son: Aspirante nuevo (primera vez), Reingreso (quien perdió la calidad de estudiante), "
                    "Transferencia interna o externa, Simultaneidad (dos programas al tiempo), Segunda carrera, "
                    "y Cambio de sede o de CREAD."
                ),
            },
            {
                "question": "¿Cuál es el contacto para inscripciones?",
                "keywords": "contacto inscripciones teléfono admisiones número llamar",
                "answer": "Sede Pamplona: 315 343 0020. Sede Villa del Rosario: 318 243 2033.",
            },
            {
                "question": "¿Cómo me inscribo a la Universidad de Pamplona?",
                "keywords": "cómo inscribirse proceso inscripción pasos registrarse matricularse nuevo",
                "answer": (
                    "Puedes inscribirte en línea a través del formulario en el portal institucional (www.unipamplona.edu.co), "
                    "en las Regionales y Sedes, o por correo certificado a la Oficina de Admisiones, Registro y Control Académico."
                ),
            },
        ],
    },
    {
        "category": "Matrícula y Costos",
        "chunks": [
            {
                "question": "¿Cuánto cuesta la matrícula en Unipamplona?",
                "keywords": "costo matrícula precio valor cuánto pagar semestre",
                "answer": (
                    "Aunque es una universidad pública, el estudiante cubre: derecho de matrícula, estampilla pro-cultura, "
                    "seguro estudiantil, derechos complementarios y capital semilla. El valor depende del programa y el "
                    "estrato socioeconómico, y se actualiza anualmente según el SMMLV. Las tablas de matrícula 2026 "
                    "están publicadas en el portal institucional."
                ),
            },
            {
                "question": "¿Existe matrícula cero en Unipamplona?",
                "keywords": "matrícula cero gratis gratuidad no pagar subsidio",
                "answer": (
                    "Sí, aplica el programa nacional de Matrícula Cero para pregrado en instituciones públicas, conforme "
                    "a los lineamientos del Ministerio de Educación Nacional y la reglamentación interna vigente."
                ),
            },
            {
                "question": "¿Qué descuentos existen en la matrícula de Unipamplona?",
                "keywords": "descuentos rebajas beneficios reducción matrícula económicos",
                "answer": (
                    "Hay descuentos del 30% para integrantes de grupos deportivos o culturales representativos, "
                    "20% adicional para quienes continúen posgrado en la misma institución, y descuentos especiales para: "
                    "hermanos matriculados simultáneamente, víctimas del conflicto armado (RUV), héroes de la nación, "
                    "personas con discapacidad, madres cabeza de familia y mayores de 62 años. "
                    "Solicitudes en: descuentos@unipamplona.edu.co"
                ),
            },
        ],
    },
    {
        "category": "Grados",
        "chunks": [
            {
                "question": "¿Cuáles son los requisitos de grado en Unipamplona?",
                "keywords": "requisitos grado graduación graduarse título diploma",
                "answer": (
                    "Los requisitos principales son: 1. Haber aprobado todos los créditos del plan de estudios. "
                    "2. Haber cumplido con el requisito de lengua extranjera. "
                    "3. Presentar y aprobar el trabajo de grado. "
                    "4. Estar a paz y salvo financiera y académicamente con la institución."
                ),
            },
            {
                "question": "¿Cuándo son las ceremonias de grado?",
                "keywords": "ceremonia grado cuándo fecha graduación acto protocolo",
                "answer": (
                    "El calendario de grados se aprueba semestralmente. Para el segundo periodo de 2026 rige el "
                    "Acuerdo N.° 024 del 21 de abril de 2026. Consulta las fechas exactas en el portal: "
                    "unipamplona.edu.co/registroycontrol"
                ),
            },
            {
                "question": "¿Cuánto tiempo tengo para graduarme?",
                "keywords": "tiempo máximo plazo límite graduarme duración carrera semestres",
                "answer": (
                    "Según el Artículo 4 del Reglamento Académico (Acuerdo 186), el tiempo máximo para obtener el título "
                    "equivale al doble del número de periodos académicos del plan de estudios vigente."
                ),
            },
        ],
    },
    {
        "category": "Reglamento Académico",
        "chunks": [
            {
                "question": "¿Qué dice el reglamento académico estudiantil?",
                "keywords": "reglamento normas reglas estatuto acuerdo 186",
                "answer": (
                    "El Reglamento Académico Estudiantil de Pregrado está establecido en el Acuerdo N.° 186 del 2 de "
                    "diciembre de 2005. Regula el comportamiento estudiantil y establece derechos y deberes. "
                    "Incluye normas sobre inscripción, calidad de estudiante, título académico, carné estudiantil y estímulos."
                ),
            },
            {
                "question": "¿Cómo se adquiere o pierde la calidad de estudiante?",
                "keywords": "calidad estudiante perder adquirir matrícula abandono",
                "answer": (
                    "La calidad de estudiante se adquiere al perfeccionar el procedimiento de matrícula, y se pierde "
                    "por graduación, abandono o bajo rendimiento, entre otras causales (Art. 2, Acuerdo 186)."
                ),
            },
            {
                "question": "¿Qué son las habilitaciones?",
                "keywords": "habilitación examen recuperar materia perdida nota",
                "answer": (
                    "El examen de habilitación se puede presentar una sola vez por periodo, para quien pierda un curso "
                    "teórico con nota final no inferior a 2.00, según el Manual de Habilitaciones."
                ),
            },
            {
                "question": "¿Qué estímulos existen por rendimiento académico?",
                "keywords": "estímulos rendimiento promedio honor mérito académico premio",
                "answer": (
                    "Los estudiantes con promedio acumulado no inferior a 3.3 pueden acceder a estímulos y privilegios "
                    "institucionales, según el Artículo 44 (Capítulo VIII) del Acuerdo 186."
                ),
            },
        ],
    },
    {
        "category": "Becas y Financiación",
        "chunks": [
            {
                "question": "¿Qué becas ofrece la Universidad de Pamplona?",
                "keywords": "becas ayuda financiera apoyo económico beca estudiar gratis",
                "answer": (
                    "La universidad ofrece: estímulos por rendimiento académico (promedio >= 3.3), becas doctorales del "
                    "Sistema General de Regalías, beca internacional de USD 2.500 para movilidad, Alianza Nortecientífica "
                    "Doctoral, programa de becas para estudiantes de bajos recursos (cobertura compartida con el departamento), "
                    "y Matrícula Cero para pregrado."
                ),
            },
            {
                "question": "¿Cómo accedo a las becas por bajo rendimiento económico?",
                "keywords": "becas bajos recursos económicos solicitar aplicar pobre",
                "answer": (
                    "El programa de becas para estudiantes regulares de bajos recursos es gestionado mediante un estudio "
                    "socioeconómico previo, con cobertura compartida entre la Universidad y el departamento de Norte de Santander."
                ),
            },
        ],
    },
    {
        "category": "Movilidad Internacional",
        "chunks": [
            {
                "question": "¿Cómo puedo hacer movilidad académica o intercambio en Unipamplona?",
                "keywords": "movilidad académica intercambio internacional estudiar afuera exterior convenio",
                "answer": (
                    "La Universidad tiene convenios con más de 70 instituciones nacionales e internacionales. El proceso es: "
                    "1. Seleccionar institución de destino. 2. Verificar requisitos con la Oficina de Internacionalización. "
                    "3. Solicitar aval al Comité de Programa. 4. El Consejo de Facultad aprueba y remite a Internacionalización. "
                    "5. Internacionalización gestiona la postulación. 6. El estudiante tramita documentos (pasaporte, visa, vacunas). "
                    "Contacto: internacionalizacion@unipamplona.edu.co"
                ),
            },
            {
                "question": "¿Cuáles son los tipos de movilidad en Unipamplona?",
                "keywords": "tipos movilidad clases formas intercambio pasantía rotación investigación",
                "answer": (
                    "Los tipos son: intercambio académico (cursar asignaturas en otra institución), práctica, pasantía "
                    "(modalidad de trabajo de grado), rotación médica, estancia de investigación, participación en eventos "
                    "académicos o culturales, y trabajo de grado investigativo."
                ),
            },
            {
                "question": "¿Cuánto cuesta la movilidad internacional?",
                "keywords": "costo movilidad precio gastos intercambio cuánto vale internacional",
                "answer": (
                    "Por regla general el estudiante asume todos los gastos (transporte, hospedaje, alimentación, seguros, visa). "
                    "La Universidad puede dar apoyo económico según disponibilidad presupuestal. La solicitud debe hacerse "
                    "con al menos un mes de anticipación."
                ),
            },
        ],
    },
    {
        "category": "Bienestar Universitario",
        "chunks": [
            {
                "question": "¿Qué servicios ofrece Bienestar Universitario en Unipamplona?",
                "keywords": "bienestar servicios salud psicología deporte cultura apoyo alimentario",
                "answer": (
                    "El Centro de Bienestar Universitario ofrece: consulta médica general, apoyo psicológico y orientación "
                    "vocacional (estrés, habilidades sociales, técnicas de estudio, prevención de deserción), apoyo "
                    "alimentario para estudiantes vulnerables, grupos deportivos y culturales representativos (con descuento "
                    "del 30% en matrícula), y programas de salud física, deporte y cultura."
                ),
            },
            {
                "question": "¿Cómo contacto a Bienestar Universitario?",
                "keywords": "contacto bienestar teléfono correo dirección bienestar universitario",
                "answer": (
                    "Sede Pamplona: Km. 1 Vía Bucaramanga, Tel: (7) 568 5303 / 568 5304, bienestaruniversitario@unipamplona.edu.co. "
                    "Sede Villa del Rosario: Autopista Internacional Vía Los Álamos, Tel: (7) 570 6966, bienestarvillarosario@unipamplona.edu.co."
                ),
            },
        ],
    },
    {
        "category": "Extranjeros",
        "chunks": [
            {
                "question": "¿Cuáles son los requisitos para estudiantes extranjeros en Unipamplona?",
                "keywords": "extranjero internacional visa requisitos foráneo otro país estudiante extranjero",
                "answer": (
                    "Los estudiantes extranjeros deben: mantener vigente la Visa Temporal de Estudiante colombiana, "
                    "inscribirse con pasaporte, convalidar ante el MEN el diploma de bachiller, presentar certificación "
                    "de pruebas equivalentes al ICFES/Saber 11 de su país, y apostillar los certificados que requieran "
                    "homologación. Contacto: carnetizacion@unipamplona.edu.co"
                ),
            },
        ],
    },
    {
        "category": "Calendario Académico",
        "chunks": [
            {
                "question": "¿Cuál es el calendario académico de Unipamplona?",
                "keywords": "calendario académico fechas semestre periodo actividades",
                "answer": (
                    "El calendario académico rige inicio y fin de clases, evaluaciones parciales, cancelación de asignaturas, "
                    "exámenes finales y fechas de grado. Se aprueba por acuerdos diferenciados por sede y modalidad. "
                    "Consulta el vigente en: unipamplona.edu.co/registroycontrol → Calendarios Vigentes."
                ),
            },
            {
                "question": "¿Cuándo empieza el semestre en Unipamplona?",
                "keywords": "cuándo empieza inicio semestre clases periodo fecha arranque",
                "answer": (
                    "Las fechas exactas varían cada periodo y se aprueban mediante acuerdos del Consejo Académico. "
                    "Para 2025-2: inicio el 1 de septiembre de 2025 (Acuerdos N.° 080-082). "
                    "Para 2026-1 y 2026-2 revisa los acuerdos vigentes en: unipamplona.edu.co/registroycontrol"
                ),
            },
        ],
    },
]


def rebuild():
    print("[*] Limpiando ChromaDB anterior...")
    if os.path.exists(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR)

    print(f"[*] Construyendo documentos con modelo: {EMBEDDING_MODEL}")
    docs = []
    for section in SECTIONS:
        for chunk in section["chunks"]:
            # Formato enriquecido: pregunta + keywords + respuesta
            content = (
                f"Categoria: {section['category']}\n"
                f"Pregunta: {chunk['question']}\n"
                f"Palabras clave: {chunk['keywords']}\n"
                f"Respuesta: {chunk['answer']}"
            )
            docs.append(Document(
                page_content=content,
                metadata={
                    "category": section["category"],
                    "question": chunk["question"],
                    "keywords": chunk["keywords"],
                },
            ))

    print(f"[OK] Total chunks: {len(docs)}")

    print("[*] Generando embeddings MULTILINGUES e indexando en ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = Chroma.from_documents(
        docs, 
        embeddings, 
        persist_directory=CHROMA_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )
    print(f"[OK] ChromaDB reconstruido con {vs._collection.count()} documentos.")

    # Pruebas de precision
    print("\n[TEST] Pruebas de precision:")
    tests = [
        ("cuando son las inscripciones", "Inscripciones y Admisi\u00f3n"),
        ("requisitos para graduarme", "Grados"),
        ("becas disponibles", "Becas y Financiaci\u00f3n"),
        ("programas de ingenieria", "Oferta Acad\u00e9mica"),
        ("costos de matricula", "Matr\u00edcula y Costos"),
        ("movilidad academica", "Movilidad Internacional"),
        ("donde queda la universidad", "Informaci\u00f3n General"),
        ("bienestar universitario", "Bienestar Universitario"),
    ]
    correct = 0
    for q, expected_cat in tests:
        results = vs.similarity_search_with_score(q, k=3)
        if results:
            doc, score = results[0]
            cat = doc.metadata.get("category", "?")
            is_match = cat == expected_cat
            mark = "[OK]" if is_match else "[FAIL]"
            if is_match:
                correct += 1
            respuesta = doc.page_content.split("Respuesta:", 1)[-1].strip()[:80]
            print(f"\n  Q: {q}")
            print(f"  {mark} Cat: {cat} (esperada: {expected_cat}) | score={score:.3f}")
            print(f"  R: {respuesta}...")

    print(f"\n[RESULT] Precision: {correct}/{len(tests)} ({100*correct/len(tests):.0f}%)")


if __name__ == "__main__":
    rebuild()
