from django.test import TestCase
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed
from datetime import datetime, timezone

User = get_user_model()


class RSSFeedModelTest(TestCase):
    def test_create_rss_feed(self):
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="https://example.com/rss.xml")
        self.assertEqual(feed.url, "https://example.com/rss.xml")
        self.assertEqual(feed.user.username, "john")


class RSSItemModelTest(TestCase):
    def test_create_rss_item(self):
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="https://example.com/rss.xml")
        pub_date = datetime(2025, 5, 5, 12, 0, 0, tzinfo=timezone.utc)
        item = feed.items.create(
            title="Example News",
            description="Example Description",
            pub_date=pub_date
        )
        self.assertEqual(item.title, "Example News")
        self.assertEqual(item.description, "Example Description")
        self.assertEqual(item.pub_date, pub_date)
