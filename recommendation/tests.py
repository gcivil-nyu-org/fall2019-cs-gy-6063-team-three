from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .forms import RecommendationForm, RecommendationRatingForm
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
        known_length=0,
        known_strength=0,
        known_location=0,
        rating_concepts=0,
        rating_creativity=0,
        rating_mathematical=0,
        rating_written=0,
        rating_oral=0,
        rating_goals=0,
        rating_socialization=0,
        rating_analyzing=0,
        rating_comment="He is smart",
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
        self.assertEqual(self.recommendation.known_length, 0)
        self.assertEqual(self.recommendation.known_strength, 0)
        self.assertEqual(self.recommendation.known_location, 0)
        self.assertEqual(self.recommendation.rating_concepts, 0)
        self.assertEqual(self.recommendation.rating_creativity, 0)
        self.assertEqual(self.recommendation.rating_mathematical, 0)
        self.assertEqual(self.recommendation.rating_written, 0)
        self.assertEqual(self.recommendation.rating_oral, 0)
        self.assertEqual(self.recommendation.rating_goals, 0)
        self.assertEqual(self.recommendation.rating_socialization, 0)
        self.assertEqual(self.recommendation.rating_analyzing, 0)
        self.assertEqual(self.recommendation.rating_comment, "He is smart")
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
        self.student = create_student(self)
        form = RecommendationForm(data=data)
        form.user_id = self.student.pk
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"first_name": "James", "last_name": "Smith", "email_address": "fake"}
        form = RecommendationForm(data=data)
        self.assertFalse(form.is_valid())

    def test_email_is_students(self):
        create_student(self)
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "hrx@gmail.com",
        }
        form = RecommendationForm(data=data)
        self.assertFalse(form.is_valid())


class RecommendationRatingFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "known_length": 1,
            "known_strength": 0,
            "known_location": 0,
            "rating_concepts": 0,
            "rating_creativity": 0,
            "rating_mathematical": 0,
            "rating_written": 0,
            "rating_oral": 0,
            "rating_goals": 0,
            "rating_socialization": 0,
            "rating_analyzing": 0,
            "rating_comment": "He is smart",
        }
        form = RecommendationRatingForm(data=data)
        self.assertTrue(form.is_valid())


class RecommendationViewTest(TestCase):
    def setUp(self):
        self.student = create_student(self)
        self.submitted_date = None
        self.recommendation = create_recommendation(self)
        self.recommendation.submitted_date = None

    def test_no_login(self):
        url = reverse("dashboard:recommendation:new_recommendation")
        response = self.client.get(url)
        self.assertTrue(response.status_code, 302)

    def test_valid_add_teacher(self):
        update_session(self.client, self.student)
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

    def test_max(self):
        self.count = 2
        update_session(self.client, self.student)
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "fake4@email.com",
        }
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_max_count_recommendations(self):
        update_session(self.client, self.student)
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "fake1@email.com",
        }
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        data = {
            "first_name": "James",
            "last_name": "Smith",
            "email_address": "fake2@email.com",
        }
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recommendation.objects.count(), 2)

    def test_invalid_add_teacher(self):
        update_session(self.client, self.student)
        data = {"first_name": "", "last_name": "", "email_address": "fake"}
        url = reverse("recommendation:new_recommendation")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Recommendation.objects.filter(
                first_name="James", last_name="Smith", email_address="fake"
            ).exists()
        )

    def test_valid_add_rating(self):
        data = {
            "known_length": 1,
            "known_strength": 0,
            "known_location": 0,
            "rating_concepts": 0,
            "rating_creativity": 0,
            "rating_mathematical": 0,
            "rating_written": 0,
            "rating_oral": 0,
            "rating_goals": 0,
            "rating_socialization": 0,
            "rating_analyzing": 0,
            "rating_comment": "He is smart",
        }
        uid64 = urlsafe_base64_encode(force_bytes(self.recommendation.pk))
        url = reverse("recommendation_rating", args=[uid64])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_add_rating(self):
        data = {
            "known_length": "HI",
            "known_strength": 0,
            "known_location": 0,
            "rating_concepts": 0,
            "rating_creativity": 0,
            "rating_mathematical": 0,
            "rating_written": 0,
            "rating_oral": 0,
            "rating_goals": 0,
            "rating_socialization": 0,
            "rating_analyzing": 0,
            "rating_comment": "He is smart",
        }
        uid64 = urlsafe_base64_encode(force_bytes(self.recommendation.pk))
        url = reverse("recommendation_rating", args=[uid64])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_no_recommendation_sent(self):
        data = {
            "known_length": 1,
            "known_strength": 0,
            "known_location": 0,
            "rating_concepts": 0,
            "rating_creativity": 0,
            "rating_mathematical": 0,
            "rating_written": 0,
            "rating_oral": 0,
            "rating_goals": 0,
            "rating_socialization": 0,
            "rating_analyzing": 0,
            "rating_comment": "He is smart",
        }
        uid64 = urlsafe_base64_encode(force_bytes(self.recommendation.pk))
        url = reverse("recommendation_rating", args=[uid64 + "B"])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_already_completed_rating(self):
        self.recommendation.submitted_date = timezone.now()
        uid64 = urlsafe_base64_encode(force_bytes(self.recommendation.pk))
        url = reverse("recommendation_rating", args=[uid64])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.recommendation.delete()
        self.student.delete()
