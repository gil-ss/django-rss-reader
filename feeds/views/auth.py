from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

class SignUpView(CreateView):
    """
    View to register a new user using Django's built-in UserCreationForm.

    On successful registration, the user is automatically logged in and redirected
    to the feed list view.
    """
    form_class = UserCreationForm
    success_url = reverse_lazy("feed-list")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """
        Log the user in after successful signup.

        Args:
            form (UserCreationForm): The validated user creation form.

        Returns:
            HttpResponse: Redirect to the success URL.
        """
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
