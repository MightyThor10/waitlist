from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import ClassWaitlist, StudentTicket
from .views import home, joinWaitlist

class ClassWaitlistModelTests(TestCase):

    def test_create_class_waitlist(self):
        user = User.objects.create_user(username='test_professor', password='testpassword')
        class_waitlist = ClassWaitlist.objects.create(
            className="Test Class",
            classCode="TEST101",
            crn=12345,
            schedule="MWF 10:00-11:00",
            sortType="FIFO",
            term="Fall 2023",
            professor=user,
            date_added="2023-04-10"
        )
        self.assertEqual(class_waitlist.className, "Test Class")

class StudentTicketModelTests(TestCase):

    def test_create_student_ticket(self):
        student = User.objects.create_user(username='test_student', password='testpassword')
        professor = User.objects.create_user(username='test_professor', password='testpassword')
        class_waitlist = ClassWaitlist.objects.create(
            className="Test Class",
            classCode="TEST101",
            crn=12345,
            schedule="MWF 10:00-11:00",
            sortType="FIFO",
            term="Fall 2023",
            professor=professor,
            date_added="2023-04-10"
        )
        student_ticket = StudentTicket.objects.create(
            class_waitlist=class_waitlist,
            date_joined="2023-04-10",
            student=student
        )
        self.assertEqual(student_ticket.student.username, "test_student")

class HomeViewTests(TestCase):

    def test_home_view_no_login(self):
        response = self.client.get(reverse('student-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log in to view your classes!")

    def test_home_view_legacy_account(self):
        user = User.objects.create_user(username='legacy_user', password='testpassword')
        self.client.login(username='legacy_user', password='testpassword')
        response = self.client.get(reverse('student-home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are not logged in as a professor or a student!")

class JoinWaitlistViewTests(TestCase):

    def test_join_waitlist_view(self):
        response = self.client.get(reverse('join-waitlist'))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, "waitlist")

class DetailViewTests(TestCase):

    def test_detail_view(self):
        user = User.objects.create_user(username='test_professor', password='testpassword')
        class_waitlist = ClassWaitlist.objects.create(
            className="Test Class",
            classCode="TEST101",
            crn=12345,
            schedule="MWF 10:00-11:00",
            sortType="FIFO",
            term="Fall 2023",
            professor=user,
            date_added="2023-04-10"
        )
        response = self.client.get(reverse('detail', args=(class_waitlist.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Class")
