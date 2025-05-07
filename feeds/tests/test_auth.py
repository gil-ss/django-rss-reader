from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthViewTests(TestCase):
    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_view_post_valid(self):
        response = self.client.post(reverse("signup"), {
            "username": "newuser",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        })
        self.assertRedirects(response, reverse("feed-list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_signup_view_post_invalid(self):
        response = self.client.post(reverse("signup"), {
            "username": "user",
            "password1": "123",
            "password2": "456",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="user").exists())

    def test_login_logout_flow(self):
        User.objects.create_user(username="test", password="secret")
        login = self.client.post(reverse("login"), {
            "username": "test",
            "password": "secret",
        })
        self.assertRedirects(login, reverse("feed-list"))
        logout = self.client.get(reverse("logout"))
        self.assertRedirects(logout, reverse("login"))
