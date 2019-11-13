from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .forms import HighSchoolApplicationForm, GENDER
from .models import HighSchoolApplication
from register.models import Student
from high_school.models import HighSchool, Program
from .views import generate_application_number
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


def create_highschool(self):
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


def create_program(self):
    return Program.objects.create(
        high_school=self.school,
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


def create_application(self):
    return HighSchoolApplication.objects.create(
        application_number=generate_application_number(
            self.student.pk, self.school.pk, self.program.pk
        ),
        user=self.student,
        first_name="Hritik",
        last_name="Roshan",
        email_address="hrx@gmail.com",
        phoneNumber="+19567801234",
        address="Brooklyn, NY",
        gender=GENDER[0],
        date_of_birth="1995-10-31",
        gpa=3.88,
        parent_name="Rakesh Roshan",
        parent_phoneNumber="+15879879870",
        school=self.school,
        program=self.program,
        is_draft=self.is_draft,
        submitted_date=self.submitted_date,
    )


def update_session(client, user):
    s = client.session
    s.update(
        {"username": user.username, "is_login": True, "user_type": UserType.STUDENT}
    )
    s.save()


class HighSchoolApplicationModelTest(TestCase):
    def setUp(self):
        self.student = create_student(self)
        self.school = create_highschool(self)
        self.program = create_program(self)
        self.submitted_date = timezone.now()
        self.is_draft = False
        self.application = create_application(self)

    def test_create(self):
        self.assertTrue(isinstance(self.application, HighSchoolApplication))
        self.assertEqual(
            self.application.application_number,
            generate_application_number(
                self.student.pk, self.school.pk, self.program.pk
            ),
        )
        self.assertEqual(self.application.first_name, "Hritik")
        self.assertEqual(self.application.last_name, "Roshan")
        self.assertEqual(self.application.email_address, "hrx@gmail.com")
        self.assertEqual(self.application.phoneNumber, "+19567801234")
        self.assertEqual(self.application.address, "Brooklyn, NY")
        self.assertEqual(self.application.gender, GENDER[0])
        self.assertEqual(self.application.date_of_birth, "1995-10-31")
        self.assertEqual(self.application.gpa, 3.88)
        self.assertEqual(self.application.parent_name, "Rakesh Roshan")
        self.assertEqual(self.application.parent_phoneNumber, "+15879879870")
        self.assertEqual(self.application.school, self.school)
        self.assertEqual(self.application.program, self.program)
        self.assertEqual(self.application.is_draft, self.is_draft)
        self.assertEqual(self.application.submitted_date, self.submitted_date)

    def test_get(self):
        response = HighSchoolApplication.objects.get(pk=self.application.pk)
        self.assertTrue(
            response.application_number, self.application.application_number
        )

    def test_delete(self):
        response = HighSchoolApplication.objects.filter(pk=self.application.pk).delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        self.student.delete()
        self.school.delete()
        self.program.delete()


class HighSchoolApplicationFormTest(TestCase):
    def setUp(self):
        self.school = create_highschool(self)
        self.program = create_program(self)

    def test_valid_form(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "+19567801234",
            "address": "Brooklyn, NY",
            "gender": GENDER[0],
            "date_of_birth": "1995-10-31",
            "gpa": 3.88,
            "parent_name": "Rakesh Roshan",
            "parent_phoneNumber": "+15879879870",
            "school": self.school.pk,
            "program": self.program.pk,
        }
        form = HighSchoolApplicationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_phoneNumber(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",  # missing country code
            "address": "Brooklyn, NY",
            "gender": GENDER[0],
            "date_of_birth": "1995-10-31",
            "gpa": 3.88,
            "parent_name": "Rakesh Roshan",
            "parent_phoneNumber": "+15879879870",
            "school": self.school.pk,
            "program": self.program.pk,
        }
        form = HighSchoolApplicationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("phoneNumber" in form.cleaned_data)

    def tearDown(self):
        self.school.delete()
        self.program.delete()


class HighSchoolApplicationViewTest(TestCase):
    def setUp(self):
        self.student = create_student(self)
        self.school = create_highschool(self)
        self.program = create_program(self)
        self.submitted_date = timezone.now()
        self.is_draft = False
        self.application = create_application(self)
        update_session(self.client, self.student)

    def test_new_application(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "+19567801234",
            "address": "Brooklyn, NY",
            "gender": GENDER[0],
            "date_of_birth": "1995-10-31",
            "gpa": 3.88,
            "parent_name": "Rakesh Roshan",
            "parent_phoneNumber": "+15879879870",
            "school": self.school.pk,
            "program": self.program.pk,
        }
        url = reverse("dashboard:application:new_application")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(
            HighSchoolApplication.objects.get(
                application_number=generate_application_number(
                    self.student.pk, self.school.pk, self.program.pk
                )
            )
        )

    def test_save_existing_application(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "+19567801234",
            "address": "Brooklyn, NY",
            "gender": GENDER[0],
            "date_of_birth": "1995-10-31",
            "gpa": 4.00,  # changed GPA
            "parent_name": "Rakesh Roshan",
            "parent_phoneNumber": "+15879879870",
            "school": self.school.pk,
            "program": self.program.pk,
        }
        url = reverse(
            "dashboard:application:draftExistingApplication", args=[self.application.pk]
        )
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(
            HighSchoolApplication.objects.get(
                application_number=generate_application_number(
                    self.student.pk, self.school.pk, self.program.pk
                )
            ).gpa,
            4.00,
        )

    def test_all_applications(self):
        url = reverse("dashboard:application:all_applications")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.application.application_number)

    def test_detail(self):
        url = reverse("dashboard:application:overview", args=[self.application.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.application.application_number)

    def tearDown(self):
        self.application.delete()
        self.student.delete()
        self.program.delete()
        self.school.delete()
