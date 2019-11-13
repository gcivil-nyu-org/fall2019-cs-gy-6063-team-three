from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .forms import RecommendationForm
from .models import Recommendation
from register.models import Student
from OneApply.constants import UserType


def create_student(self):
    return Student.objects.create(
        first_name="Hritik",
        last_name="Roshan",
        email_address="hrx@gmail.com",
        username="hritik",
        password="hritikRoshan@10",
        current_school="NYU",
        borough="MN",
    )


def create_recommendation(self):
    return Recommendation.objects.create(
        user=self.student,
        first_name="James",
        last_name="Smith",
        email_address="fake@email.com",
        recommendation="TEST RECOMMEND",
        submitted_date=self.submitted_date,
    )


def update_session(client, user):
    s = client.session
    s.update(
        {"username": user.username, "is_login": True, "user_type": UserType.STUDENT}
    )
    s.save()


class RecommendationModelTest(TestCase):
    def setUp(self):
        self.student = create_student(self)
        self.submitted_date = timezone.now()
        self.recommendation = create_recommendation(self)

    def test_create(self):
        self.assertTrue(isinstance(self.recommendation, Recommendation))
        self.assertEqual(self.recommendation.first_name, "James")
        self.assertEqual(self.recommendation.last_name, "Smith")
        self.assertEqual(self.recommendation.email_address, "fake@email.com")
        self.assertEqual(self.recommendation.recommendation, "TEST RECOMMEND")
        self.assertEqual(self.recommendation.submitted_date, self.submitted_date)

    def test_get(self):
        response = Recommendation.objects.get(pk=self.recommendation.pk)
        self.assertTrue(response.email_address, self.recommendation.email_address)

    def test_delete(self):
        response = Recommendation.objects.filter(pk=self.recommendation.pk).delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        self.student.delete()


class RecommendationFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "fake@email.com",
        }
        form = RecommendationForm(data=data)
        self.assertTrue(form.is_valid())


class RecommendationViewTest(TestCase):
    def setUp(self):
        self.student = create_student(self)
        self.submitted_date = timezone.now()
        self.recommendation = create_recommendation(self)
        update_session(self.client, self.student)

    def test_valid_add_teacher(self):
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "fake@email.com",
        }
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            Recommendation.objects.filter(
                first_name="James", last_name="Smith", email_address="fake@email.com"
            ).exists()
        )

    def test_invalid_add_teacher(self):
        data = {"first_name": "", "last_name": "", "email_address": "fake"}
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Recommendation.objects.filter(
                first_name="James", last_name="Smith", email_address="fake"
            ).exists()
        )

    def tearDown(self):
        self.recommendation.delete()
        self.student.delete()
