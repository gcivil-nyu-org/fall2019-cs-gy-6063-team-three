from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import HighSchoolApplicationForm, GENDER
from .models import HighSchoolApplication
from register.models import Student


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
            school="NYU",
            program="CS",
            is_draft=self.is_draft,
            submitted_date=self.submitted_date,
        )

    def setUp(self):
        self.student = create_student(self)
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
        self.assertEqual(application.school, "NYU")
        self.assertEqual(application.program, "CS")
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


class HighSchoolApplicationFormTest(TestCase):
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
            "school": "NYU",
            "program": "CS",
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
            "school": "NYU",
            "program": "CS",
        }
        form = HighSchoolApplicationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("phoneNumber" in form.cleaned_data)


class HighSchoolApplicationViewTest(TestCase):
    def setUp(self):
        self.student = create_student(self)

    def test_valid_draft_application(self):
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
            "school": "NYU",
            "program": "CS",
        }
        url = reverse("application:draftApplication", args=[self.student.id])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(
            HighSchoolApplication.objects.get(
                application_number=str(self.student.pk) + "NYU" + "CS"
            )
        )
