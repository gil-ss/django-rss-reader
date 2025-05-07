from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from feeds.models import RSSFeed

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

    def test_feed_create_view_post_creates_feed(self):
        form_data = {"url": "http://example.com/rss"}
        response = self.client.post(reverse("feed-add"), data=form_data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(RSSFeed.objects.count(), 1)
        self.assertEqual(RSSFeed.objects.first().user, self.user)

    def test_feed_create_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("feed-add"))
        self.assertRedirects(response, "/login/?next=/add/")