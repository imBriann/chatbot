# 🚀 Reporte de Pruebas de Integración y Funcionamiento (Extendido)

Se ha completado la validación en vivo de la integración entre el backend (FastAPI) y el frontend (React) del chatbot utilizando un agente de navegación web automatizado y un script de pruebas automatizadas sobre la API REST.

---

### 🎥 Animación / Video de la Prueba Interactiva

A continuación se presenta la grabación de la sesión de interacción en el navegador web del chatbot, demostrando el flujo de comunicación y la recuperación de información precisa:

![Grabación en vivo del chat interactivo](C:/Users/Asly%20Acuña/.gemini/antigravity/brain/f47356c2-7fbd-4833-bdda-c332aab35b78/test_chatbot_flow_1781663219616.webp)

---

### 📊 Resultados de la Suite de 15 Preguntas Funcionales

Se ejecutó un script en caliente que envía 15 preguntas clave directamente a la API REST del chatbot (`http://127.0.0.1:8001/api/chat/message`) para auditar la precisión y la relevancia de las respuestas devueltas por el motor híbrido (Semántico + Palabras Clave):

| # | Pregunta de Prueba | Respuesta del Chatbot | Confianza | Estado |
|---|---|---|:---:|:---:|
| 1 | **¿Cuándo son las fechas de inscripción?** | Las fechas de inscripción se aprueban semestralmente mediante acuerdo del Consejo Académico. Para el segundo periodo de 2026 rigen los Acuerdos N.° 021 y 022 del 21 de abril de 2026. Consulta las fechas vigentes en: unipamplona.edu.co/registroycontrol → Calendarios Académicos Vigentes. | 0.85 | **PASSED** ✅ |
| 2 | **¿Cómo es el proceso para inscribirme en línea?** | Puedes inscribirte en línea a través del formulario en el portal institucional (www.unipamplona.edu.co), en las Regionales y Sedes, o por correo certificado a la Oficina de Admisiones, Registro y Control Académico. | 0.15 | **PASSED** (Híbrido) ✅ |
| 3 | **¿Qué documentos o requisitos me piden para la admisión?** | Los requisitos generales son: diligenciar el formulario de inscripción en línea, subir fotografía reciente (fondo azul, tamaño 3x4), ser bachiller graduado con diploma o acta de grado, haber presentado las Pruebas Saber 11, presentar documento de identidad y recibo de servicios públicos del lugar de residencia. | 0.85 | **PASSED** ✅ |
| 4 | **¿Cuáles son los requisitos para estudiantes extranjeros?** | Los estudiantes extranjeros deben: mantener vigente la Visa Temporal de Estudiante colombiana, inscribirse con pasaporte, convalidar ante el MEN el diploma de bachiller, presentar certificación de pruebas equivalentes al ICFES/Saber 11 de su país, y apostillar los certificados que requieran homologación. Contacto: carnetizacion@unipamplona.edu.co | 0.85 | **PASSED** ✅ |
| 5 | **¿Cómo funciona la movilidad académica o los intercambios?** | La Universidad tiene convenios con más de 70 instituciones nacionales e internacionales. El proceso es: 1. Seleccionar institución de destino. 2. Verificar requisitos con la Oficina de Internacionalización. 3. Solicitar aval al Comité de Programa. 4. El Consejo de Facultad aprueba y remite a Internacionalización. | 0.85 | **PASSED** ✅ |
| 6 | **¿Quién asume los costos de una movilidad internacional?** | Por regla general el estudiante asume todos los gastos (transporte, hospedaje, alimentación, seguros, visa). La Universidad puede dar apoyo económico según disponibilidad presupuestal. La solicitud debe hacerse con al menos un mes de anticipación. | 0.85 | **PASSED** ✅ |
| 7 | **¿De cuánto es el valor del semestre o matrícula?** | Aunque es una universidad pública, el estudiante cubre: derecho de matrícula, estampilla pro-cultura, seguro estudiantil, derechos complementarios y capital semilla. El valor depende del programa y el estrato socioeconómico, y se actualiza anualmente según el SMMLV. | 0.85 | **PASSED** ✅ |
| 8 | **¿Qué becas o apoyos económicos ofrece la universidad?** | La universidad ofrece: estímulos por rendimiento académico (promedio >= 3.3), becas doctorales del Sistema General de Regalías, beca internacional de USD 2.500 para movilidad, Alianza Nortecientífica Doctoral, programa de becas para estudiantes de bajos recursos, y Matrícula Cero para pregrado. | 0.85 | **PASSED** ✅ |
| 9 | **¿Cuáles son los descuentos disponibles para la matrícula?** | Hay descuentos del 30% para integrantes de grupos deportivos o culturales representativos, 20% adicional para quienes continúen posgrado en la misma institución, y descuentos especiales para: hermanos matriculados simultáneamente, víctimas del conflicto armado (RUV), héroes de la nación, personas con discapacidad... | 0.85 | **PASSED** ✅ |
| 10 | **¿Aplica el beneficio de matrícula cero?** | Sí, aplica el programa nacional de Matrícula Cero para pregrado en instituciones públicas, conforme a los lineamientos del Ministerio de Educación Nacional y la reglamentación interna vigente. | 0.85 | **PASSED** ✅ |
| 11 | **¿Cuáles son los requisitos para poderme graduar?** | Los requisitos principales son: 1. Haber aprobado todos los créditos del plan de estudios. 2. Haber cumplido con el requisito de lengua extranjera. 3. Presentar y aprobar el trabajo de grado. 4. Estar a paz y salvo financiera y académicamente con la institución. | 0.62 | **PASSED** ✅ |
| 12 | **¿Cuándo se realizan las ceremonias de grado?** | El calendario de grados se aprueba semestralmente. Para el segundo periodo de 2026 rige el Acuerdo N.° 024 del 21 de abril de 2026. Consulta las fechas exactas en el portal: unipamplona.edu.co/registroycontrol | 0.85 | **PASSED** ✅ |
| 13 | **¿Dónde quedan ubicadas las diferentes sedes?** | La sede principal está en Pamplona, Norte de Santander (Km 1 Vía Bucaramanga, Ciudad Universitaria). También tiene sede en Villa del Rosario (Autopista Internacional Vía Los Álamos, Villa Antigua) y en Cúcuta. | 0.10 | **PASSED** (Híbrido) ✅ |
| 14 | **¿Qué servicios de salud y apoyo brinda Bienestar Universitario?** | El Centro de Bienestar Universitario ofrece: consulta médica general, apoyo psicológico y orientación vocacional (estrés, habilidades sociales, técnicas de estudio, prevención de deserción), apoyo alimentario para estudiantes vulnerables, grupos deportivos y culturales representativos... | 0.85 | **PASSED** ✅ |
| 15 | **¿Qué programas de pregrado ofrece la universidad?** | La Universidad ofrece 43 programas de pregrado, de los cuales 12 cuentan con Acreditación en Alta Calidad. Se distribuyen en modalida presencial (Pamplona y Villa del Rosario–Cúcuta), a distancia e híbrida. | 0.85 | **PASSED** ✅ |

---

### 📷 Evidencia Adicional

![Conversación interactiva sobre movilidad académica en el frontend](C:/Users/Asly%20Acuña/.gemini/antigravity/brain/f47356c2-7fbd-4833-bdda-c332aab35b78/test_results_1781663343066.png)
