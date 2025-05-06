from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from feeds.models import RSSFeed
from feeds.services import parse_and_save_feed
from django.core.paginator import Paginator


class FeedListView(LoginRequiredMixin, ListView):
    """
    View that displays all RSS feeds associated with the currently authenticated user.

    Attributes:
        model (Model): The Django model associated with this view.
        template_name (str): The path to the HTML template.
        context_object_name (str): The name of the object list in the template context.

    Methods:
        get_queryset(): Returns only the feeds owned by the current user.
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

    On successful creation, it triggers the parsing and storage of items from the feed.

    Attributes:
        model (Model): The Django model used for creating a new instance.
        fields (list): The fields to be included in the form.
        template_name (str): The path to the HTML template.
        success_url (str): URL to redirect to after successful creation.

    Methods:
        form_valid(form): Attaches user and triggers feed parsing.
    """
    model = RSSFeed
    fields = ["url"]
    template_name = "feeds/feed_form.html"
    success_url = reverse_lazy("feed-list")

    def form_valid(self, form):
        """
        Called when the submitted form is valid.

        Args:
            form (ModelForm): The validated form instance.

        Returns:
            HttpResponse: The HTTP response after processing.
        """
        form.instance.user = self.request.user
        response = super().form_valid(form)
        parse_and_save_feed(self.object)
        return response


class FeedDetailView(LoginRequiredMixin, DetailView):
    """
    View that shows a single RSS feed and its associated items, with pagination.

    Attributes:
        model (Model): The Django model for the detail view.
        template_name (str): The HTML template used to render the view.
        context_object_name (str): The name of the feed in the template context.

    Methods:
        get_queryset(): Limits access to feeds owned by the current user.
        get_context_data(**kwargs): Adds paginated items to the context.
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
        page_obj = paginator.get_page(page_number)

        context["page_obj"] = page_obj
        return context
