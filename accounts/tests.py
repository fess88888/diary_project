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

    def test_login_logout_flow(self):
        get_user_model().objects.create_user(
            username="alice", password="Secret123!"
        )

        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alice", "password": "Secret123!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("_auth_user_id", self.client.session)
