from django.test import TestCase
from django.utils import timezone

from .forms import HighSchoolApplicationForm, GENDER
from .models import HighSchoolApplication
from register.models import Student
from high_school.models import HighSchool, Program


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


class HighSchoolApplicationModelTest(TestCase):
    def create_application(self):
        return HighSchoolApplication.objects.create(
            application_number=str(self.student.pk) + "NYU" + "CS",
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

    def setUp(self):
        self.student = create_student(self)
        self.school = create_highschool(self)
        self.program = create_program(self)
        self.submitted_date = timezone.now()
        self.is_draft = False

    def test_create(self):
        application = self.create_application()
        self.assertTrue(isinstance(application, HighSchoolApplication))
        self.assertEqual(
            application.application_number, str(self.student.pk) + "NYU" + "CS"
        )
        self.assertEqual(application.first_name, "Hritik")
        self.assertEqual(application.last_name, "Roshan")
        self.assertEqual(application.email_address, "hrx@gmail.com")
        self.assertEqual(application.phoneNumber, "+19567801234")
        self.assertEqual(application.address, "Brooklyn, NY")
        self.assertEqual(application.gender, GENDER[0])
        self.assertEqual(application.date_of_birth, "1995-10-31")
        self.assertEqual(application.gpa, 3.88)
        self.assertEqual(application.parent_name, "Rakesh Roshan")
        self.assertEqual(application.parent_phoneNumber, "+15879879870")
        self.assertEqual(application.school, self.school)
        self.assertEqual(application.program, self.program)
        self.assertEqual(application.is_draft, self.is_draft)
        self.assertEqual(application.submitted_date, self.submitted_date)

    def test_get(self):
        application = self.create_application()
        response = HighSchoolApplication.objects.get(id=application.id)
        self.assertTrue(response.application_number, application.application_number)

    def test_delete(self):
        application = self.create_application()
        response = HighSchoolApplication.objects.filter(id=application.id).delete()
        self.assertIsNotNone(response)

    def tearDown(self):
        self.student.delete()
        self.school.delete()


class HighSchoolApplicationFormTest(TestCase):
    def setUp(self):
        self.school = create_highschool(self)

    # TODO : giving error for school due to foreign key object
    # def test_valid_form(self):
    #     data = {
    #         "first_name": "Hritik",
    #         "last_name": "Roshan",
    #         "email_address": "hrx@gmail.com",
    #         "phoneNumber": "+19567801234",
    #         "address": "Brooklyn, NY",
    #         "gender": GENDER[0],
    #         "date_of_birth": "1995-10-31",
    #         "gpa": 3.88,
    #         "parent_name": "Rakesh Roshan",
    #         "parent_phoneNumber": "+15879879870",
    #         "school": self.school,
    #         "program": "CS",
    #     }
    #     form = HighSchoolApplicationForm(data=data)
    #     self.assertTrue(form.is_valid())

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
            "school": self.school,
            "program": "CS",
        }
        form = HighSchoolApplicationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("phoneNumber" in form.cleaned_data)

    def tearDown(self):
        self.school.delete()


# TODO test views
