from playwright.sync_api import sync_playwright
import re


def clean_text(text: str) -> str:
    # ANSI + control chars
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    text = re.sub(r'\^\[[A-Z]', '', text)
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', ' ', text)

    # espacios múltiples
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def scrape_job_description(url: str) -> str:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox"]
            )

            page = browser.new_page()

            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # esperar render real (mejor que sleep fijo)
            page.wait_for_timeout(2000)

            # intento 1: secciones típicas de job boards
            selectors = [
                "main",
                "[role='main']",
                ".job-description",
                ".description",
                "#job-description"
            ]

            content = None

            for selector in selectors:
                try:
                    if page.locator(selector).count() > 0:
                        content = page.locator(selector).inner_text()
                        break
                except:
                    continue

            # fallback global
            if not content:
                content = page.inner_text("body")

            browser.close()

            return clean_text(content)

    except Exception as e:
        print(f"[Scraping error]: {e}")
        return None