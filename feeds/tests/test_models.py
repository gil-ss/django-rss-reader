from django.test import TestCase
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed

User = get_user_model()


class RSSFeedModelTest(TestCase):
    def test_create_rss_feed(self):
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="https://example.com/rss.xml")

        self.assertEqual(feed.url, "https://example.com/rss.xml")
        self.assertEqual(feed.user.username, "john")
