from django.test import TestCase, RequestFactory
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .models import ClassWaitlist, StudentTicket
from .views import home, joinWaitlist, joinwaitlistNotification, leavewaitlistNotification, createWaitlistNotification, move_studentNotification, move_student, update_waitlist_statusNotification, update_waitlist_status, audit_student_positions

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

class ArchivedClassTest(TestCase):

    def test_home_view_no_login(self):
        user = User.objects.create_user(username='test_professor', password='testpassword')
        class_waitlist = ClassWaitlist.objects.create(
            className="Test Class",
            classCode="TEST101",
            crn=12345,
            schedule="MWF 10:00-11:00",
            sortType="FIFO",
            term="Fall 2023",
            professor=user,
            date_added="2023-04-10",
            archived=True,
        )
        response = self.client.get(reverse('waitlist-archive'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Archived Classes")


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

class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com', first_name='Test', last_name='User')

        self.professor = User.objects.create_user(username='professor', password='testpassword', email='professor@example.com', first_name='John', last_name='Doe')

        self.waitlist = ClassWaitlist.objects.create(
            className='Test Class',
            classDescription='Test Class Description',
            classCode='TEST123',
            crn=12345,
            schedule='MWF 10:00-11:00',
            sortType='Test',
            term='Fall 2023',
            professor=self.professor,
            date_added='2023-04-30',
            closed=False,
            anonymous_waitlist=False,
            archived=False
        )

    def test_joinwaitlist_notification(self):
        joinwaitlistNotification(self.user, self.waitlist)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You have joined a waitlist!')

    def test_leavewaitlist_notification(self):
        student_ticket = StudentTicket.objects.create(class_waitlist=self.waitlist, date_joined='2023-04-30', student=self.user, position=1, waitlist_status='p')
        leavewaitlistNotification(self.user, student_ticket)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You have left a waitlist!')

    def test_createwaitlist_notification(self):
        createWaitlistNotification(self.professor, 'Test Class', 'Test Class Description', 'TEST123', 12345, 'MWF 10:00-11:00', 'Test', 'Fall 2023', '2023-04-30', False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Waitlist Created!')



class MoveStudentNotificationTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user1 = User.objects.create_user(username='testuser1', password='testpassword', email='testuser1@example.com', first_name='Test1', last_name='User1')
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword', email='testuser2@example.com', first_name='Test2', last_name='User2')
        self.professor = User.objects.create_user(username='professor', password='testpassword', email='professor@example.com', first_name='John', last_name='Doe')

        self.waitlist = ClassWaitlist.objects.create(
            className='Test Class',
            classDescription='Test Class Description',
            classCode='TEST123',
            crn=12345,
            schedule='MWF 10:00-11:00',
            sortType='Test',
            term='Fall 2023',
            professor=self.professor,
            date_added='2023-04-30',
            closed=False,
            anonymous_waitlist=False,
            archived=False
        )

        self.ticket1 = StudentTicket.objects.create(class_waitlist=self.waitlist, date_joined='2023-04-30', student=self.user1, position=1, waitlist_status='p')
        self.ticket2 = StudentTicket.objects.create(class_waitlist=self.waitlist, date_joined='2023-04-30', student=self.user2, position=2, waitlist_status='p')

    def test_move_student_notification(self):
        move_studentNotification(self.ticket1, "up")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'You have been moved up in a waitlist!')

        move_studentNotification(self.ticket2, "down")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'You have been moved down in a waitlist!')

    def test_move_student(self):
        request = self.factory.get('/studenthome/')
        request.user = self.professor

        # Move student1 up (no change)
        response = move_student(request, self.ticket1.id, "up")
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        ticket2 = get_object_or_404(StudentTicket, id=self.ticket2.id)
        self.assertEqual(ticket1.position, 1)
        self.assertEqual(ticket2.position, 2)

        # Move student1 down
        response = move_student(request, self.ticket1.id, "down")
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        ticket2 = get_object_or_404(StudentTicket, id=self.ticket2.id)
        self.assertEqual(ticket1.position, 2)
        self.assertEqual(ticket2.position, 1)

    def test_update_waitlist_status_notification(self):
        update_waitlist_statusNotification(self.ticket1, "p")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your waitlist status has been changed!')
        update_waitlist_statusNotification(self.ticket1, "a")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Your waitlist status has been changed!')

        update_waitlist_statusNotification(self.ticket1, "r")
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[2].subject, 'Your waitlist status has been changed!')

    def test_update_waitlist_status(self):
        request = self.factory.get('/studenthome/')
        request.user = self.professor

        response = update_waitlist_status(request, self.ticket1.id, "a")
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        self.assertEqual(ticket1.waitlist_status, "a")

        response = update_waitlist_status(request, self.ticket1.id, "r")
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        self.assertEqual(ticket1.waitlist_status, "r")

        response = update_waitlist_status(request, self.ticket1.id, "p")
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        self.assertEqual(ticket1.waitlist_status, "p")

    def test_audit_student_positions(self):
        self.ticket1.position = 3
        self.ticket1.save()

        audit_student_positions(self.waitlist)
        ticket1 = get_object_or_404(StudentTicket, id=self.ticket1.id)
        ticket2 = get_object_or_404(StudentTicket, id=self.ticket2.id)
        self.assertEqual(ticket1.position, 2)
        self.assertEqual(ticket2.position, 1)