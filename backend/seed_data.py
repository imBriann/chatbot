from database import SessionLocal
from models import Knowledge, Intent

def seed():
    db = SessionLocal()
    
    # Intenciones
    intents = [
        Intent(name="saludo", description="El usuario saluda", examples=["Hola", "Buenos días", "Qué tal"]),
        Intent(name="requisitos_grado", description="Pregunta por grado", examples=["¿Qué necesito para graduarme?", "requisitos de grado"]),
        Intent(name="inscripcion", description="Proceso de inscripción", examples=["¿Cómo me inscribo?", "Quiero estudiar allá"]),
    ]
    for intent in intents:
        if not db.query(Intent).filter_by(name=intent.name).first():
            db.add(intent)
            
    # Conocimiento
    faqs = [
        Knowledge(
            category="Inscripciones",
            question="¿Cuáles son los pasos para inscribirme en la Universidad de Pamplona?",
            answer="Para inscribirte debes: 1. Ingresar a la página oficial. 2. Llenar el formulario de pre-inscripción. 3. Pagar el pin de inscripción en el banco autorizado. 4. Registrar el pago y seleccionar el programa de interés."
        ),
        Knowledge(
            category="Grados",
            question="¿Cuáles son los requisitos de grado?",
            answer="Los requisitos principales son: 1. Haber aprobado todos los créditos del plan de estudios. 2. Haber cumplido con el requisito de lengua extranjera. 3. Presentar y aprobar el trabajo de grado. 4. Estar a paz y salvo financiera y académicamente."
        ),
        Knowledge(
            category="Extranjeros",
            question="¿Cuáles son los requisitos para estudiantes extranjeros?",
            answer="Los estudiantes extranjeros deben presentar su título de bachiller convalidado por el Ministerio de Educación de Colombia, pasaporte vigente, visa de estudiante y seguro médico internacional válido."
        ),
        Knowledge(
            category="Matrícula",
            question="¿Cuándo son las fechas de pago de matrícula?",
            answer="Las fechas de pago varían por semestre. Generalmente el pago ordinario se realiza un mes antes de iniciar clases. Estos datos corresponden al periodo vigente; consulta siempre la página de Registro y Control Académico para actualizaciones."
        ),
        Knowledge(
            category="General",
            question="¿Dónde está ubicada la Universidad de Pamplona?",
            answer="La sede principal se encuentra en Pamplona, Norte de Santander, Colombia. También cuenta con sedes en Cúcuta y Villa del Rosario."
        )
    ]
    
    for faq in faqs:
        if not db.query(Knowledge).filter_by(question=faq.question).first():
            db.add(faq)
            
    db.commit()
    db.close()
    print("Base de datos poblada con éxito.")

if __name__ == "__main__":
    seed()
