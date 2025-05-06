from unittest.mock import patch
from types import SimpleNamespace
from django.test import TestCase
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed, RSSItem
from feeds.services import parse_and_save_feed

User = get_user_model()

class RSSFeedParserTest(TestCase):
    @patch("feeds.services.rss_parser.feedparser.parse")
    def test_parse_and_save_feed_creates_items(self, mock_parse):
        # Simulate the result of feedparser.parse() as an object with an .entries attribute
        mock_parse.return_value = SimpleNamespace(
            entries=[
                {
                    "title": "Mock Title",
                    "description": "Mock Description",
                    "published_parsed": (2025, 5, 5, 12, 0, 0, 0, 0, 0),
                }
            ]
        )
        # Create a test user and associated RSS feed
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="http://mock.url/rss")

        # Call the service function to parse and save items for the feed
        parse_and_save_feed(feed)

        # Fetch the saved item and validate its content
        item = RSSItem.objects.get(feed=feed)
        self.assertEqual(item.title, "Mock Title")
        self.assertEqual(item.description, "Mock Description")
