from django.contrib.auth.models import User
from django.test import TestCase

from e_diary.models import Diary, Grade


class YourGradesViewTests(TestCase):
    def test_login_page_is_available(self):
        response = self.client.get("/accounts/login/")

        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get("/newgrade/")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_view_recreates_missing_diary_for_authenticated_user(self):
        user = User.objects.create_user(username="recreate-user", password="pass12345")
        Diary.objects.filter(user_profile=user).delete()

        self.client.force_login(user)
        response = self.client.get("/newgrade/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Diary.objects.filter(user_profile=user).exists())
        self.assertContains(response, "No grades yet.")

    def test_view_shows_existing_grades(self):
        user = User.objects.create_user(username="student", password="pass12345")
        diary = Diary.objects.get(user_profile=user)
        Grade.objects.create(user_profile=diary, grade=12, messege="Excellent work")

        self.client.force_login(user)
        response = self.client.get("/newgrade/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "12")
        self.assertContains(response, "Excellent work")

    def test_diary_is_created_for_new_users(self):
        user = User.objects.create_user(username="new-user", password="pass12345")

        self.assertTrue(Diary.objects.filter(user_profile=user).exists())
