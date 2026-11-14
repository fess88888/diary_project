from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Entry


class EntryModelTests(TestCase):
    def test_str_returns_title(self):
        user = get_user_model().objects.create_user(
            username="alice", password="Secret123!"
        )
        entry = Entry.objects.create(
            user=user, title="Понедельник", content="Начал новую неделю."
        )
        self.assertEqual(str(entry), "Понедельник")


class EntryViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="Secret123!"
        )
        self.other = get_user_model().objects.create_user(
            username="bob", password="Secret123!"
        )
        self.entry = Entry.objects.create(
            user=self.user, title="Тест", content="Текст записи"
        )

    def login(self, username):
        self.client.login(username=username, password="Secret123!")

    def test_create_entry(self):
        self.login("alice")
        response = self.client.post(reverse("diary:entry-create"), {
            "title": "Новая запись",
            "content": "Содержимое новой записи",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Entry.objects.filter(title="Новая запись").exists()
        )

    def test_list_shows_only_own_entries(self):
        self.login("bob")
        Entry.objects.create(user=self.other, title="Чужая", content="...")
        response = self.client.get(reverse("diary:entry-list"))
        self.assertContains(response, "Чужая")
        self.assertNotContains(response, "Тест")

    def test_update_entry(self):
        self.login("alice")
        response = self.client.post(
            reverse("diary:entry-update", args=[self.entry.pk]),
            {"title": "Обновлено", "content": "Новый текст"},
        )
        self.assertEqual(response.status_code, 302)
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Обновлено")

    def test_delete_entry(self):
        self.login("alice")
        response = self.client.post(
            reverse("diary:entry-delete", args=[self.entry.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Entry.objects.filter(pk=self.entry.pk).exists()
        )

    def test_search_filters_entries(self):
        self.login("alice")
        Entry.objects.create(
            user=self.user, title="Погода", content="Дождь весь день"
        )
        response = self.client.get(
            reverse("diary:entry-list"), {"q": "Погода"}
        )
        self.assertContains(response, "Погода")
        self.assertNotContains(response, "Текст записи")
