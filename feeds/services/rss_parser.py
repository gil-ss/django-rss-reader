import feedparser
from datetime import datetime
from feeds.models import RSSItem

def parse_and_save_feed(feed):
    parsed = feedparser.parse(feed.url)
    for entry in parsed.entries:
        published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")

        pub_date = (
            datetime(*published_parsed[:6]) if published_parsed else None
        )

        if not entry.get("title"):
            continue  # Skip malformed entries

        RSSItem.objects.get_or_create(
            feed=feed,
            title=entry["title"],
            defaults={
                "description": entry.get("description", ""),
                "pub_date": pub_date
            }
        )
