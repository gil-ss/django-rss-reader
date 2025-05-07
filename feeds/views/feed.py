import feedparser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from feeds.models import RSSFeed
from feeds.services import parse_and_save_feed


class FeedListView(LoginRequiredMixin, ListView):
    """
    View that displays all RSS feeds associated with the currently authenticated user.

    Attributes:
        model (Model): The Django model associated with this view.
        template_name (str): The path to the HTML template.
        context_object_name (str): The name of the object list in the template context.
    """
    model = RSSFeed
    template_name = "feeds/feed_list.html"
    context_object_name = "feeds"

    def get_queryset(self):
        """
        Filters the feed list to include only those that belong to the current user.

        Returns:
            QuerySet: A queryset of RSSFeed objects.
        """
        return RSSFeed.objects.filter(user=self.request.user)


class FeedCreateView(LoginRequiredMixin, CreateView):
    """
    View that allows a logged-in user to add a new RSS feed.

    Validates the URL by checking if the parsed RSS has content.
    On success, saves the feed and parses its items.

    Attributes:
        model (Model): The Django model used for creating a new instance.
        fields (list): The fields to be included in the form.
        template_name (str): The path to the HTML template.
        success_url (str): URL to redirect to after successful creation.
    """
    model = RSSFeed
    fields = ["url"]
    template_name = "feeds/feed_form.html"
    success_url = reverse_lazy("feed-list")

    def form_valid(self, form):
        """
        Called when the submitted form is valid.

        Checks if the URL points to a valid RSS feed.
        If valid, saves the feed and triggers item parsing.
        Otherwise, shows an error message and redisplays the form.

        Args:
            form (ModelForm): The validated form instance.

        Returns:
            HttpResponse: The HTTP response after processing.
        """
        form.instance.user = self.request.user
        url = form.cleaned_data["url"]

        parsed = feedparser.parse(url)
        if not parsed.entries or parsed.bozo:
            messages.error(self.request, "Invalid RSS feed URL.")
            return self.form_invalid(form)

        response = super().form_valid(form)
        parse_and_save_feed(self.object)
        messages.success(self.request, "Feed added successfully!")
        return response


class FeedDetailView(LoginRequiredMixin, DetailView):
    """
    View that shows a single RSS feed and its associated items, with pagination.
    """
    model = RSSFeed
    template_name = "feeds/feed_detail.html"
    context_object_name = "feed"

    def get_queryset(self):
        """
        Ensures the user can only view their own feeds.

        Returns:
            QuerySet: Filtered queryset of RSSFeed objects.
        """
        return RSSFeed.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        """
        Adds paginated RSS items to the context.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data for the template.
        """
        context = super().get_context_data(**kwargs)
        items = self.object.items.all().order_by("-pub_date")
        paginator = Paginator(items, 5)  # Show 5 items per page
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)
        return context


class FeedUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to update an existing RSSFeed. Only the owner can update.
    """
    model = RSSFeed
    fields = ["url"]
    template_name = "feeds/feed_form.html"
    success_url = reverse_lazy("feed-list")

    def get_queryset(self):
        """
        Restricts editing to feeds owned by the current user.

        Returns:
            QuerySet: A queryset limited to the user's feeds.
        """
        return RSSFeed.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Called when the submitted form is valid for an update.

        Displays a success message.

        Args:
            form (ModelForm): The validated form instance.

        Returns:
            HttpResponse: The HTTP response after processing.
        """
        messages.success(self.request, "Feed updated successfully.")
        return super().form_valid(form)


class FeedDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete an RSSFeed. Only the owner can delete.
    """
    model = RSSFeed
    template_name = "feeds/feed_confirm_delete.html"
    success_url = reverse_lazy("feed-list")

    def get_queryset(self):
        """
        Restricts deletion to feeds owned by the current user.

        Returns:
            QuerySet: A queryset limited to the user's feeds.
        """
        return RSSFeed.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handles POST request to delete the feed.

        Returns:
            HttpResponseRedirect: Redirects to feed list with a success message.
        """
        messages.add_message(self.request, messages.WARNING, "Feed deleted successfully.")
        return super().post(request, *args, **kwargs)



