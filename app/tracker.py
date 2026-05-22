import json
import uuid
import re
import os
from datetime import datetime

from app.matcher import evaluate_match
from app.parser import load_text
from app.cv_generator import generate_cv
from app.pdf_generator import generate_pdf
from app.pdf_parser import load_pdf_text


# =========================
# Config
# =========================

THRESHOLD = 75
DB_PATH = "data/tracking.json"
CV_TXT_PATH = "data/cvs/cv.txt"
CV_PDF_PATH = "data/cvs/cv.pdf"
OUTPUT_DIR = "data/output"


STATES = [
    "Not applied",
    "Applied",
    "First interview",
    "Technical interview",
    "Last interview",
    "Offer received",
    "Rejected"
]


# =========================
# DB helpers
# =========================

def load_db():
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =========================
# Utils
# =========================

def sanitize_filename(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', text)


def extract_score(evaluation: str) -> int:
    try:
        parsed = json.loads(evaluation)
        return int(parsed.get("match_score", 0))
    except Exception:
        return 0


def load_cv():
    """
    Carga el CV automáticamente desde PDF o TXT
    """
    try:
        if os.path.exists(CV_PDF_PATH):
            print("📄 Usando CV en PDF...")
            return load_pdf_text(CV_PDF_PATH)

        elif os.path.exists(CV_TXT_PATH):
            print("📄 Usando CV en TXT...")
            return load_text(CV_TXT_PATH)

        else:
            raise FileNotFoundError("No se encontró cv.pdf ni cv.txt en data/cvs/")

    except Exception as e:
        raise Exception(f"Error cargando CV: {e}")


# =========================
# Core
# =========================

def add_job(title, company, job_description=None):
    data = load_db()

    cv_text = load_cv()

    evaluation = None
    optimized_cv = None
    pdf_path = None
    score_value = 0

    if job_description:
        print("🧠 Evaluando match...")

        try:
            evaluation = evaluate_match(cv_text, job_description)
            score_value = extract_score(evaluation)
        except Exception as e:
            print(f"❌ Error evaluando match: {e}")

        print(f"📊 Score: {score_value}")

        # =========================
        # Generación de CV si pasa threshold
        # =========================
        if score_value >= THRESHOLD:
            print("🚀 Generando CV optimizado...")

            try:
                optimized_cv_raw = generate_cv(cv_text, job_description)

                try:
                    optimized_cv = json.loads(optimized_cv_raw)
                except Exception as e:
                    print(f"❌ Error parseando JSON del CV: {e}")
                    optimized_cv = None

                if optimized_cv:
                    safe_title = sanitize_filename(title)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    pdf_path = f"{OUTPUT_DIR}/{safe_title}_{timestamp}.pdf"

                    generate_pdf(optimized_cv, pdf_path)

                    print(f"📄 PDF generado en: {pdf_path}")

            except Exception as e:
                print(f"❌ Error generando CV/PDF: {e}")

    # =========================
    # Crear job SIEMPRE
    # =========================
    job = {
        "id": str(uuid.uuid4()),
        "title": title,
        "company": company,
        "status": "Not applied",
        "description": job_description,
        "evaluation": evaluation,
        "match_score": score_value,
        "optimized_cv": optimized_cv,
        "pdf_path": pdf_path,
        "created_at": datetime.now().isoformat(),
        "updated_at": None
    }

    data.append(job)
    save_db(data)

    return job


def list_jobs():
    return load_db()


def update_status(job_id, new_status):
    if new_status not in STATES:
        raise ValueError(f"Estado inválido. Usa uno de: {STATES}")

    data = load_db()
    updated = False

    for job in data:
        if job["id"] == job_id:
            job["status"] = new_status
            job["updated_at"] = datetime.now().isoformat()
            updated = True
            break

    if not updated:
        raise ValueError("Job ID no encontrado")

    save_db(data)


# =========================
# Extra útil
# =========================

def get_job(job_id):
    data = load_db()
    for job in data:
        if job["id"] == job_id:
            return job
    return None


def open_pdf(job_id):
    job = get_job(job_id)

    if not job:
        print("❌ Job no encontrado")
        return

    if not job.get("pdf_path"):
        print("⚠️ Este job no tiene PDF generado")
        return

    os.system(f"xdg-open {job['pdf_path']}")