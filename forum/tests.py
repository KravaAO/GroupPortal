from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, include, path
from django.conf import settings

from .models import Thread, Post

settings.ROOT_URLCONF = __name__
urlpatterns = [
    path("forum/", include("forum.urls")),
]

User = get_user_model()


class ForumTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)

    def test_thread_creation_by_staff(self):
        self.client.login(username="staff", password="pass")
        response = self.client.post(reverse("forum:create_thread"), {"title": "Test thread"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Thread.objects.filter(title="Test thread").exists())

    def test_thread_not_created_by_regular(self):
        self.client.login(username="user", password="pass")
        response = self.client.post(reverse("forum:create_thread"), {"title": "Bad"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Thread.objects.filter(title="Bad").exists())

    def test_post_validation(self):
        thread = Thread.objects.create(title="T1", created_by=self.staff)
        self.client.login(username="user", password="pass")
        response = self.client.post(
            reverse("forum:thread_detail", args=[thread.pk]), {"body": "   "}
        )
        self.assertContains(response, "Message cannot be empty.")

    def test_post_creation(self):
        thread = Thread.objects.create(title="T2", created_by=self.staff)
        self.client.login(username="user", password="pass")
        response = self.client.post(
            reverse("forum:thread_detail", args=[thread.pk]), {"body": "Hello"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(thread=thread, body="Hello").exists())
