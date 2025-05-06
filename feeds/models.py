from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RSSFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")
    url = models.URLField()

    def __str__(self):
        return self.url
