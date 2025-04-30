from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from users.forms import UserRegisterForm

class UsersViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    # === Registration ===
    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIsInstance(response.context["form"], UserRegisterForm)

    def test_register_view_post_valid(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("expense-list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_view_post_invalid(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "password1": "123",
            "password2": "321",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertFalse(User.objects.filter(username="newuser").exists())

    # === Login ===
    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_view_post_valid(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("expenses-home"))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    # === Logout ===
    def test_logout_view(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    # === Profile: View and Update ===
    def test_profile_view_get(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_view_post_info_valid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("profile") + "?tab=info", {
            "username": "updateduser",
            "email": "updated@example.com"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_profile_view_post_info_invalid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("profile") + "?tab=info", {
            "username": "",  # Invalid (required)
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")

    def test_profile_view_post_password_valid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("profile") + "?tab=password", {
            "old_password": "testpass",
            "new_password1": "newstrongpassword123",
            "new_password2": "newstrongpassword123",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("profile"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newstrongpassword123"))

    def test_profile_view_post_password_invalid(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(reverse("profile") + "?tab=password", {
            "old_password": "wrongpass",
            "new_password1": "123",
            "new_password2": "321",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
print("Running users/tests/test_views.py")