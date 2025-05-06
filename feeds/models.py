from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RSSFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")
    url = models.URLField()
    def __str__(self):
        return self.url


class RSSItem(models.Model):
    feed = models.ForeignKey(RSSFeed, on_delete=models.CASCADE, related_name="items")
    title = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField()
    def __str__(self):
        return self.title
