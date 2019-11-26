# Create your tests here.
from django.utils import timezone

from django.test import TestCase
from django.urls import reverse

from OneApply.constants import UserType
from application.models import HighSchoolApplication
from high_school.models import HighSchool, Program
from register.models import Admin_Staff, Student


def create_student():
    return Student.objects.create(
        id=1,
        username="studentone",
        first_name="John",
        last_name="Doe",
        email_address="john.doe@gmail.com",
        current_school="NYU",
        borough="B",
        password="Something@123",
    )


def create_admission_staff(school):
    return Admin_Staff.objects.create(
        id=1,
        username="jwang",
        first_name="Jenny",
        last_name="Wang",
        email_address="jenny.wang@gmail.com",
        school=school,
        supervisor_email="jack.w@nyu.edu",
        password="Jenny@1234",
    )


def create_school():
    return HighSchool.objects.create(
        dbn="DBN1",
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


def create_program(school):
    return Program.objects.create(
        high_school=school,
        name="Academy of Engineering",
        code="AE123",
        description="New York State approved CTE Program that leads to national "
        "certification aligned with industry standards and a "
        "CTE-endorsed Regents Diploma. Interdisciplinary "
        "project-based curriculum includes coursework in Introduction "
        "to Engineering & Design, Digital Electronics, Principles of "
        "Engineering, and Engineering Design & Development.",
        number_of_seats=70,
        offer_rate=0,
    )


def create_application(student, school, program):
    return HighSchoolApplication.objects.create(
        id=1,
        application_number=754376,
        user=student,
        first_name="Nikhil",
        last_name="Miller",
        email_address="j.miller@nyu.edu",
        phoneNumber="+19134587025",
        address="125 Bleeker Street",
        gender="Male",
        date_of_birth="1995-04-23",
        gpa=3.5,
        parent_name="Jonah Miller",
        parent_phoneNumber="+19135670125",
        school=school,
        program=program,
        submitted_date=timezone.now(),
        is_draft=False,
    )


def common_setup():
    student = create_student()
    school = create_school()
    program = create_program(school)
    create_admission_staff(school)
    create_application(student, school, program)


def update_session(client, username, user_type=UserType.ADMIN_STAFF):
    s = client.session
    s.update({"username": username, "is_login": True, "user_type": user_type})
    s.save()


class AdmissionsIndexViewTest(TestCase):
    def setUp(self):
        common_setup()

    # This test needs to be added after adding sessions
    def test_no_admin_login(self):
        # Test without creating admin user
        url = reverse("dashboard:admissions:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_valid_admin_login(self):
        # Check for admin staff who doesnt exist
        update_session(self.client, "jwang")
        url = reverse("dashboard:admissions:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertContains(response, "754376")

    def test_invalid_admin_login(self):
        # Check for admin staff who doesnt exist
        update_session(self.client, "abcd", UserType.STUDENT)
        url = reverse("dashboard:admissions:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertContains(
            response,
            "Whoa! Something seems wrong. You're trying to access " "this page ",
        )


class AdmissionsDetailViewTest(TestCase):
    def setUp(self):
        common_setup()

    def test_invalid_application_no_admin_login(self):
        # Test without creating admin user
        url = reverse("dashboard:admissions:detail", args=[11])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_invalid_application_admin_login(self):
        # Test without creating admin user
        update_session(self.client, "jwang")
        url = reverse("dashboard:admissions:detail", args=[11])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Oops! We couldn't find what you're looking for..."
        )

    def test_valid_application_no_admin_login(self):
        url = reverse("dashboard:admissions:detail", args=[1])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_valid_application_admin_login(self):
        update_session(self.client, "jwang")
        url = reverse("dashboard:admissions:detail", args=[1])
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertContains(response, "754376")

    def test_valid_application_student_login(self):
        update_session(self.client, "jwang", UserType.STUDENT)
        url = reverse("dashboard:admissions:detail", args=[1])
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertNotContains(response, "754376")
