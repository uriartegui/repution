import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timezone


def _clean_html(text: str) -> str:
    return BeautifulSoup(text, "html.parser").get_text(separator=" ", strip=True)


def fetch_google_news(keyword: str) -> list[dict]:
    url = f"https://news.google.com/rss/search?q={keyword}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    feed = feedparser.parse(url)
    results = []

    for entry in feed.entries[:10]:
        title = _clean_html(entry.get("title", ""))
        results.append({
            "source": "google_news",
            "source_url": entry.get("link", ""),
            "author": entry.get("source", {}).get("title", "Google News"),
            "content": title,
            "collected_at": datetime.now(timezone.utc),
        })

    return results
