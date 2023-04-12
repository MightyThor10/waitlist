from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from users.forms import UserRegisterForm

class UserRegisterFormTests(TestCase):

    def test_valid_form(self):
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@email.wm.edu',
            'password1': 'strong_password123',
            'password2': 'strong_password123'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_email_domain(self):
        form = UserRegisterForm({
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'strong_password123',
            'password2': 'strong_password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

class RegisterViewTests(TestCase):

    def setUp(self):
        self.student_group = Group.objects.create(name='Student')

    def test_register_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_view_creates_user_and_adds_to_group(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@email.wm.edu',
            'password1': 'strong_password123',
            'password2': 'strong_password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.get(username='johndoe')
        self.assertIsNotNone(user)

        group = Group.objects.get(name='Student')
        self.assertTrue(user.groups.filter(name='Student').exists())


class ProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='johndoe',
            password='strong_password123',
            email='johndoe@email.wm.edu'
        )


    def test_profile_view_uses_correct_template(self):
        self.client.login(username='johndoe', password='strong_password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
