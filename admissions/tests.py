# Create your tests here.
from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from admissions.models import HighSchoolApplication
from high_school.models import HighSchool
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
        id=11,
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
        graduation_rate=80
    )


def create_application(student, school):
    return HighSchoolApplication.objects.create(
        id=1,
        application_number=754376,
        user=student,
        first_name="Nikhil",
        last_name="Miller",
        email_address="j.miller@nyu.edu",
        phoneNumber="9134587025",
        address="125 Bleeker Street",
        gender="Male",
        date_of_birth="1995-04-23",
        gpa=3.5,
        parent_name="Jonah Miller",
        parent_phoneNumber="9135670125",
        school=school,
        program="Science",
        submitted_date=datetime.now()
    )


def common_setup():
    student = create_student()
    school = create_school()
    create_admission_staff(school)
    create_application(student, school)


class AdmissionsIndexViewTest(TestCase):

    def setUp(self):
        common_setup()

    def test_invalid_admin(self):
        # Test without creating admin user
        url = reverse("admissions:index", args=[1])
        response = self.client.post(url)
        self.assertContains(response, "No applications are available.")

    def test_valid_admin(self):
        # Check for admin staff who doesnt exist
        url = reverse("admissions:index", args=[11])
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertContains(response, "754376")


class AdmissionsDetailViewTest(TestCase):
    def setUp(self):
        common_setup()

    def test_invalid_application(self):
        # Test without creating admin user
        url = reverse("admissions:detail", args=[11])
        response = self.client.post(url)
        self.assertContains(response,
                            "The application you are looking for doesn't exist.")

    def test_valid_admin(self):
        # Check for admin staff who doesnt exist
        url = reverse("admissions:detail", args=[1])
        response = self.client.post(url)
        self.assertEquals(response.status_code, 200)
        # Check if application number created is available in the rendered page
        self.assertContains(response, "754376")
