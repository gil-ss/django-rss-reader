from django.test import TestCase
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed, RSSItem
from feeds.services import parse_and_save_feed

User = get_user_model()

class RSSFeedParserTest(TestCase):
    def test_parse_and_save_feed_creates_items(self):
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="https://example.com/fake-feed.xml")
        parse_and_save_feed(feed)
        self.assertTrue(RSSItem.objects.filter(feed=feed).exists())
