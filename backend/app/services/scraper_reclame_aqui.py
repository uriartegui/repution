import asyncio, json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from datetime import datetime, timezone


def _clean(text: str) -> str:
    return BeautifulSoup(text, "html.parser").get_text(strip=True)


async def _fetch_page_async(company_slug: str, page_num: int, existing_urls: set) -> tuple[list[dict], bool]:
    """Retorna (resultados, encontrou_duplicata)."""
    results = []
    found_duplicate = False

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            locale="pt-BR",
        )
        page = await context.new_page()

        url = f"https://www.reclameaqui.com.br/empresa/{company_slug}/lista-reclamacoes/?pagina={page_num}"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)

        next_data_raw = await page.evaluate("() => JSON.stringify(window.__NEXT_DATA__)")
        await browser.close()

        if not next_data_raw:
            return results, found_duplicate

        next_data = json.loads(next_data_raw)
        complaints = next_data.get("props", {}).get("pageProps", {}).get("complaints", {})
        items = complaints.get("LAST", [])

        for item in items:
            title = _clean(item.get("title", ""))
            description = _clean(item.get("description", ""))
            content = f"{title}. {description}".strip(" .")
            url_slug = item.get("url", "")
            full_url = f"https://www.reclameaqui.com.br/{company_slug}/{url_slug}/" if url_slug else ""

            if full_url and full_url in existing_urls:
                found_duplicate = True
                break

            if content:
                results.append({
                    "source": "reclame_aqui",
                    "source_url": full_url,
                    "author": "Consumidor anônimo",
                    "content": content,
                    "collected_at": datetime.now(timezone.utc),
                })

    return results, found_duplicate


def fetch_reclame_aqui(keyword: str, existing_urls: set = None, max_pages: int = 10) -> list[dict]:
    """
    Coleta reclamações do Reclame Aqui.
    - existing_urls: URLs já no banco (para coleta incremental)
    - max_pages: limite de páginas a buscar
    """
    if existing_urls is None:
        existing_urls = set()

    slug = keyword.lower().replace(" ", "-")
    all_results = []

    for page_num in range(1, max_pages + 1):
        results, found_duplicate = asyncio.run(_fetch_page_async(slug, page_num, existing_urls))
        all_results.extend(results)

        if found_duplicate or not results:
            break

    return all_results
