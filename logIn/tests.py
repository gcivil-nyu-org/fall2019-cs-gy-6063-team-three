from django.test import TestCase
from django.urls import reverse

from .forms import LoginForm
from OneApply.constants import UserType
from register.models import Student


class LoginFormTest(TestCase):
    def test_valid_form(self):
        data = {"username": "hritik", "password": "hritikRoshan@10"}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"username": "hritik", "password": ""}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


class LoginViewTest(TestCase):
    def create_student(self):
        return Student.objects.create(
            first_name="Hritik",
            last_name="Roshan",
            email_address="hrx@gmail.com",
            phoneNumber="9567801234",
            username="hritik",
            password="hritikRoshan@10",
            current_school="NYU",
            borough="MN",
        )

    def setUp(self):
        self.student = self.create_student()

    def test_valid_login_student(self):
        data = {"username": "hritik", "password": "hritikRoshan@10"}
        url = reverse("logIn:login_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def test_invalid_login_student(self):
        data = {"username": "hritik", "password": "hritikRoshan@230"}
        url = reverse("logIn:login_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def tearDown(self):
        self.student.delete()
