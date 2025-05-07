import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed
from unittest.mock import patch
from types import SimpleNamespace


User = get_user_model()

class FeedListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret")
        self.other_user = User.objects.create_user(username="alice", password="secret")
        self.feed1 = RSSFeed.objects.create(user=self.user, url="http://example.com/rss1")
        self.feed2 = RSSFeed.objects.create(user=self.user, url="http://example.com/rss2")
        RSSFeed.objects.create(user=self.other_user, url="http://example.com/rss3")
        self.client.login(username="john", password="secret")

    def test_feed_list_view_shows_only_user_feeds(self):
        response = self.client.get(reverse("feed-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feeds/feed_list.html")
        feeds = list(response.context["feeds"])
        self.assertIn(self.feed1, feeds)
        self.assertIn(self.feed2, feeds)
        self.assertEqual(len(feeds), 2)


class FeedDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret")
        self.other_user = User.objects.create_user(username="alice", password="secret")
        self.feed = RSSFeed.objects.create(user=self.user, url="http://example.com/rss")
        self.other_feed = RSSFeed.objects.create(user=self.other_user, url="http://example.com/rss2")
        self.client.login(username="john", password="secret")

    def test_feed_detail_view_shows_user_feed(self):
        url = reverse("feed-detail", kwargs={"pk": self.feed.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feeds/feed_detail.html")
        self.assertEqual(response.context["feed"], self.feed)

    def test_feed_detail_view_for_other_user_returns_404(self):
        url = reverse("feed-detail", kwargs={"pk": self.other_feed.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class FeedCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret")
        self.client.login(username="john", password="secret")

    def test_feed_create_view_get(self):
        response = self.client.get(reverse("feed-add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feeds/feed_form.html")

    @patch("feeds.views.feed.feedparser.parse")
    def test_feed_create_view_post_creates_feed(self, mock_parse):
        mock_parse.return_value = SimpleNamespace(
            entries=[{
                "title": "Sample",
                "summary": "A sample item",
                "link": "http://example.com/sample",
                "published_parsed": time.strptime("2025-05-07 10:00:00", "%Y-%m-%d %H:%M:%S"),
                "media_thumbnail": [{"url": "http://example.com/image.jpg"}],
            }],
            feed={"title": "Test Feed"},
            bozo=False
        )
        response = self.client.post(reverse("feed-add"), {"url": "http://example.com/rss"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RSSFeed.objects.count(), 1)
        self.assertEqual(RSSFeed.objects.first().user, self.user)

    def test_feed_create_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("feed-add"))
        self.assertRedirects(response, "/login/?next=/add/")


class FeedUpdateDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john", password="secret")
        self.other_user = User.objects.create_user(username="alice", password="secret")
        self.feed = RSSFeed.objects.create(user=self.user, url="http://example.com/rss")
        self.other_feed = RSSFeed.objects.create(user=self.other_user, url="http://example.com/rss2")
        self.client.login(username="john", password="secret")

    def test_get_update_view_as_owner(self):
        response = self.client.get(reverse("feed-edit", kwargs={"pk": self.feed.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feeds/feed_form.html")

    def test_post_update_view_as_owner(self):
        response = self.client.post(reverse("feed-edit", kwargs={"pk": self.feed.pk}), {
            "url": "http://updated.com/rss"
        })
        self.assertRedirects(response, reverse("feed-list"))
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.url, "http://updated.com/rss")

    def test_update_view_other_user_returns_404(self):
        response = self.client.get(reverse("feed-edit", kwargs={"pk": self.other_feed.pk}))
        self.assertEqual(response.status_code, 404)

    def test_get_delete_view_as_owner(self):
        response = self.client.get(reverse("feed-delete", kwargs={"pk": self.feed.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "feeds/feed_confirm_delete.html")

    def test_post_delete_view_as_owner(self):
        response = self.client.post(reverse("feed-delete", kwargs={"pk": self.feed.pk}))
        self.assertRedirects(response, reverse("feed-list"))
        self.assertFalse(RSSFeed.objects.filter(pk=self.feed.pk).exists())

    def test_delete_view_other_user_returns_404(self):
        response = self.client.get(reverse("feed-delete", kwargs={"pk": self.other_feed.pk}))
        self.assertEqual(response.status_code, 404)
