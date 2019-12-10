from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from high_school.models import HighSchool
from .forms import LoginForm
from OneApply.constants import UserType
from register.models import Student, Admin_Staff


class LoginFormTest(TestCase):
    def test_valid_form(self):
        data = {"username": "hritik", "password": "hritikRoshan@10"}
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"username": "hritik", "password": ""}
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())


class LoginStudentViewTest(TestCase):
    def create_student(self):
        return Student.objects.create(
            first_name="Hritik",
            last_name="Roshan",
            email_address="hrx@gmail.com",
            username="hritik",
            password=make_password("hritikRoshan@10"),
            current_school="NYU",
            borough="MN",
            is_active=True,
        )

    def setUp(self):
        self.student = self.create_student()

    def test_valid_login_student(self):
        data = {"username": "hritik", "password": "hritikRoshan@10"}
        url = reverse("logIn:login_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def test_invalid_login_student(self):
        data = {"username": "hritik", "password": "hritikRoshan@230"}
        url = reverse("logIn:login_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def test_invalid_username_login_student(self):
        data = {"username": "hritick", "password": "hritikRoshan@10"}
        url = reverse("logIn:login_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def tearDown(self):
        self.student.delete()


class LoginAdminStaffViewTest(TestCase):
    def create_school(self):
        return HighSchool.objects.create(
            dbn="1",
            school_name="GMU",
            boro="B",
            overview_paragraph="Overview1",
            neighborhood="Neighborhood1",
            location="1, ABCD Street",
            phone_number=9173924885,
            school_email="school@gmu.com",
            website="www.gmu.com",
            total_students=1000,
            start_time=123,
            end_time=124,
            graduation_rate=80,
        )

    def create_admin_staff(self):
        hs = self.create_school()
        return Admin_Staff.objects.create(
            first_name="Hritik",
            last_name="Roshan",
            email_address="hrx@gmail.com",
            username="hritik",
            password=make_password("hritikRoshan@10"),
            school=hs,
            supervisor_email="hrx@gmail.com",
            is_verified_employee=True,
            is_active=True,
        )

    def setUp(self):
        self.admin_staff = self.create_admin_staff()

    def test_valid_login_admin_staff(self):
        data = {"username": "hritik", "password": "hritikRoshan@10"}
        url = reverse("logIn:login_user", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(Admin_Staff.objects.get(username="hritik"))

    def test_invalid_login_admin_staff(self):
        data = {"username": "hritik", "password": "hritikRoshan@12"}
        url = reverse("logIn:login_user", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Admin_Staff.objects.get(username="hritik"))

    def test_invalid_username_admin_staff(self):
        data = {"username": "hritick", "password": "hritikRoshan@12"}
        url = reverse("logIn:login_user", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Admin_Staff.objects.get(username="hritik"))

    def tearDown(self):
        self.admin_staff.delete()
