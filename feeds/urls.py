from django.urls import path
from feeds.views.feed import FeedListView, FeedCreateView, FeedDetailView

urlpatterns = [
    path("", FeedListView.as_view(), name="feed-list"),
    path("add/", FeedCreateView.as_view(), name="feed-add"),
    path("<int:pk>/", FeedDetailView.as_view(), name="feed-detail"),
]
