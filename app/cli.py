import argparse
import re

from app.tracker import add_job, list_jobs, update_status, STATES
from app.scraper import scrape_job_description


# =========================
# Utils
# =========================
def clean_text(text: str) -> str:
    # elimina secuencias raras tipo ^[E
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    text = re.sub(r'\^\[[A-Z]', '', text)
    return text.strip()


def read_multiline_input():
    print("\n📄 Pega el Job Description")
    print("👉 Escribe 'END' en una nueva línea para terminar\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    return "\n".join(lines)


# =========================
# CLI
# =========================
def main():
    parser = argparse.ArgumentParser(description="CV Tracker CLI")
    subparsers = parser.add_subparsers(dest="command")

    # add
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--title", required=True)
    add_parser.add_argument("--company", required=True)
    add_parser.add_argument("--url", required=False)

    # list
    subparsers.add_parser("list")

    # update
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True)
    update_parser.add_argument("--status", required=True, choices=STATES)

    args = parser.parse_args()

    # =========================
    # ADD
    # =========================
    if args.command == "add":
        job_description = None

        # scraping
        if args.url:
            print("🔎 Haciendo scraping...")
            job_description = scrape_job_description(args.url)

            if job_description:
                print("✅ Scraping exitoso")
            else:
                print("⚠️ Falló scraping, se pedirá input manual")

        # fallback manual
        if not job_description:
            job_description = read_multiline_input()

        # limpieza
        job_description = clean_text(job_description)

        print("\n🧹 Texto limpiado (preview):\n")
        print(job_description[:500] + "\n...")

        print("\n🧠 Enviando al modelo (esto puede tardar unos segundos)...")

        job = add_job(
            args.title,
            args.company,
            job_description
        )

        print("\n✅ Vacante agregada:\n")
        print(job)

    # =========================
    # LIST
    # =========================
    elif args.command == "list":
        jobs = list_jobs()
        for j in jobs:
            print(f"{j['id']} | {j['company']} | {j['title']} | {j['status']}")

    # =========================
    # UPDATE
    # =========================
    elif args.command == "update":
        update_status(args.id, args.status)
        print("Estado actualizado")

    else:
        print("Comando no válido")


if __name__ == "__main__":
    main()