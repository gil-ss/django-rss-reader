from unittest.mock import patch, Mock
from django.test import TestCase
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed, RSSItem
from feeds.services import parse_and_save_feed
import time

User = get_user_model()

class RSSFeedParserTest(TestCase):
    @patch("feeds.services.rss_parser.feedparser.parse")
    def test_parse_and_save_feed_creates_items(self, mock_parse):
        # Mock the parsed feed structure
        mock_parsed = Mock()
        mock_parsed.feed = {"title": "Mock Feed Title"}
        mock_parsed.entries = [{
            "title": "Mock Title",
            "summary": "Mock Description",
            "link": "http://example.com/test-item",
            "published_parsed": time.struct_time((2025, 5, 5, 12, 0, 0, 0, 0, 0)),
            "media_thumbnail": [{"url": "http://example.com/image.jpg"}],
        }]
        mock_parse.return_value = mock_parsed

        # Setup test user and feed
        user = User.objects.create_user(username="john", password="secret")
        feed = RSSFeed.objects.create(user=user, url="http://mock.url/rss")

        # Execute parser
        parse_and_save_feed(feed)

        # Assert that item was saved
        item = RSSItem.objects.get(feed=feed)
        self.assertEqual(item.title, "Mock Title")
        self.assertEqual(item.description, "Mock Description")
        self.assertEqual(item.link, "http://example.com/test-item")
        self.assertEqual(item.image_url, "http://example.com/image.jpg")
        self.assertIsNotNone(item.pub_date)
