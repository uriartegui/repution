import asyncio
from playwright.async_api import async_playwright
from datetime import datetime, timezone


async def _fetch_reviews_async(business_name: str) -> list[dict]:
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            locale="pt-BR",
        )
        page = await context.new_page()

        try:
            await page.goto(
                f"https://www.google.com/maps/search/{business_name.replace(' ', '+')}",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            await page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Erro ao abrir Google Maps: {e}")
            await browser.close()
            return results

        # Se ainda está na busca, clica no primeiro resultado
        if "/search/" in page.url:
            try:
                await page.click("a[href*='/maps/place/']", timeout=8000)
                await page.wait_for_timeout(2000)
            except Exception:
                await browser.close()
                return results

        # Clica na aba de avaliações
        try:
            reviews_tab = page.get_by_role("tab").filter(has_text="Avalia")
            await reviews_tab.click(timeout=8000)
            await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Aba de avaliações não encontrada: {e}")

        # Scroll pra carregar reviews
        scrollable = page.locator("div[role='main']")
        for _ in range(5):
            await scrollable.press("End")
            await page.wait_for_timeout(800)

        # Extrai reviews
        reviews = await page.query_selector_all("div[data-review-id]")
        print(f"Reviews encontradas: {len(reviews)}")

        for review in reviews[:10]:
            try:
                # Expande texto completo se houver botão "mais"
                more_btn = await review.query_selector("button[aria-label='Ver mais']")
                if more_btn:
                    await more_btn.click()
                    await page.wait_for_timeout(300)

                text_el = await review.query_selector("span[data-expandable-section]")
                if not text_el:
                    text_el = await review.query_selector(".MyEned span")
                text = await text_el.inner_text() if text_el else ""

                author_el = await review.query_selector(".d4r55")
                author = await author_el.inner_text() if author_el else "Anônimo"

                stars_el = await review.query_selector("span[role='img']")
                stars_label = await stars_el.get_attribute("aria-label") if stars_el else ""

                if text.strip():
                    results.append({
                        "source": "google_maps",
                        "source_url": page.url,
                        "author": author.strip(),
                        "content": f"{stars_label}. {text.strip()}" if stars_label else text.strip(),
                        "collected_at": datetime.now(timezone.utc),
                    })
            except Exception:
                continue

        await browser.close()

    return results


def fetch_google_maps(business_name: str) -> list[dict]:
    return asyncio.run(_fetch_reviews_async(business_name))
