from app.parser import load_text
from app.matcher import evaluate_match

def main():
    cv = load_text("data/cvs/cv.txt")
    job = load_text("data/jobs/job.txt")

    result = evaluate_match(cv, job)

    print("\n=== RESULTADO ===\n")
    print(result)


if __name__ == "__main__":
    main()