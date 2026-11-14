from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def test_signup_creates_user_and_logs_in(self):
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password1": "SuperSecret123!",
            "password2": "SuperSecret123!",
        }
        response = self.client.post(reverse("accounts:signup"), data)
        if response.status_code == 200:
            self.fail(f"Ошибки формы: {response.context['form'].errors}")

        self.assertTrue(
            get_user_model().objects.filter(username="testuser").exists()
        )
        self.assertRedirects(response, reverse("diary:entry-list"))

    def test_home_shows_login_for_anonymous(self):
        response = self.client.get("/")
        self.assertContains(response, "Войти")


class DiaryAccessTests(TestCase):
    def test_entry_list_requires_login(self):
        response = self.client.get(reverse("diary:entry-list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
