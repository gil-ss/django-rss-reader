from django.urls import path
from feeds.views.feed import FeedListView, FeedCreateView, FeedDetailView, FeedUpdateView, FeedDeleteView


urlpatterns = [
    path("", FeedListView.as_view(), name="feed-list"),
    path("add/", FeedCreateView.as_view(), name="feed-add"),
    path("<int:pk>/", FeedDetailView.as_view(), name="feed-detail"),
    path("<int:pk>/edit/", FeedUpdateView.as_view(), name="feed-edit"),
    path("<int:pk>/delete/", FeedDeleteView.as_view(), name="feed-delete"),
]
print("urls.py carregado")