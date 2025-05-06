import feedparser
from datetime import datetime, timezone
from feeds.models import RSSItem

def parse_and_save_feed(feed):
    """
    Parses the RSS feed URL and stores entries in the database.

    Extracts title, description, publication date, link, and thumbnail image.
    Ensures no duplicate items are created by matching titles per feed.
    """
    parsed = feedparser.parse(feed.url)

    # Set feed title from channel metadata
    feed_title = parsed.feed.get("title", "").strip()
    if feed_title:
        feed.title = feed_title
        feed.save()

    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        if not title:
            continue  # skip entries without a title

        pub_date = None
        if entry.get("published_parsed"):
            pub_date = datetime(*entry["published_parsed"][:6], tzinfo=timezone.utc)

        description = entry.get("summary", "").strip()
        link = entry.get("link", "").strip()

        image_url = None
        if "media_thumbnail" in entry:
            media = entry["media_thumbnail"]
            if isinstance(media, list) and "url" in media[0]:
                image_url = media[0]["url"]

        RSSItem.objects.get_or_create(
            feed=feed,
            title=title,
            defaults={
                "description": description,
                "pub_date": pub_date,
                "link": link,
                "image_url": image_url
            }
        )
