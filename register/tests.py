from django.test import TestCase
from django.urls import reverse

from .models import Student
from .forms import StudentRegisterForm
from OneApply.constants import UserType


class StudentModelTest(TestCase):
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

    def test_create(self):
        student = self.create_student()
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(student.email_address, "hrx@gmail.com")
        self.assertEqual(student.username, "hritik")
        self.assertEqual(student.password, "hritikRoshan@10")

    def test_get(self):
        student = self.create_student()
        response = Student.objects.get(username="hritik")
        self.assertTrue(response.username, student.username)

    def test_delete(self):
        self.create_student()
        response = Student.objects.filter(username="hritik").delete()
        self.assertIsNotNone(response)


class StudentFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@10",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikroshan@",
            "confirm_password": "hritikroshan@",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("input_password" in form.cleaned_data)

    def test_mismatch_password(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@1",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("confirm_password" in form.cleaned_data)


class StudentViewTest(TestCase):
    def test_valid_register_student(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@10",
            "current_school": "NYU",
            "borough": "MN",
        }
        url = reverse("register:register_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def test_invalid_register_student(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@575",
            "current_school": "NYU",
            "borough": "MN",
        }
        url = reverse("register:register_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.filter(username="hritik").count(), 0)
