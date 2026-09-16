```python
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

RSS_URL = "https://news.google.com/rss/search?q=finance+OR+economy+OR+markets&hl=en-US&gl=US&ceid=US:en"


def fetch_news():
    print("正在获取金融新闻...")

    request = urllib.request.Request(
        RSS_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read()

    root = ET.fromstring(data)

    news = []

    for item in root.findall("./channel/item")[:10]:
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")

        news.append({
            "title": title,
            "link": link,
            "published": pub_date
        })

    result = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "source": "Google News RSS",
        "news": news
    }

    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"成功获取 {len(news)} 条新闻")
    print("新闻已保存到 news.json")


if __name__ == "__main__":
    fetch_news()
