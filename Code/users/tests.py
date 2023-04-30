from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .forms import UserRegisterForm, StudentProfileForm, CustomPasswordChangeForm
from .views import register, send_welcome_email, change_passwordNotification, profile
from .models import StudentProfile
from django.core import mail

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



class TestNotificationSystem(TestCase):
    def setUp(self):
        self.client = Client()
        self.group1 = Group.objects.create(name="Professor")
        self.group2 = Group.objects.create(name="Student")
        self.user1 = User.objects.create_user(username='user1', email='user1@wm.edu', password='testpassword', first_name='User', last_name='One')
        self.user1.groups.add(self.group2)
        self.user2 = User.objects.create_user(username='user2', email='user2@wm.edu', password='testpassword', first_name='User', last_name='Two')
        self.user2.groups.add(self.group1)


    def test_send_welcome_email(self):
        mail.outbox = []
        send_welcome_email(self.user1, self.group2.name)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to the Waitlist Management System')
        self.assertIn('Dear User One', mail.outbox[0].body)

        mail.outbox = []
        send_welcome_email(self.user2, self.group1.name)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Welcome to the Waitlist Management System')
        self.assertIn('Dear Professor User Two', mail.outbox[0].body)

    def test_change_passwordNotification(self):
        mail.outbox = []
        change_passwordNotification(self.user1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'IMPORTANT: Your password has been changed')
        self.assertIn('Dear User One', mail.outbox[0].body)

    def test_register(self):
        response = self.client.post('/register/', {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'newuser@wm.edu',
            'password1': 'newuserpassword',
            'password2': 'newuserpassword',
        })
        user = User.objects.filter(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertTrue(user.groups.filter(name='Student').exists())

    def test_profile(self):
        self.client.login(username='user1', password='testpassword')
        response = self.client.post('/profile/', {
            'update_profile': '',
            'preferred_name': 'Preferred',
            'academic_status': 'SR',
            'major': 'Computer Science',
        })
        self.assertEqual(response.status_code, 302)

        updated_profile = StudentProfile.objects.get(user=self.user1)
        self.assertEqual(updated_profile.preferred_name, 'Preferred')
        self.assertEqual(updated_profile.academic_status, 'SR')
        self.assertEqual(updated_profile.major, 'Computer Science')
