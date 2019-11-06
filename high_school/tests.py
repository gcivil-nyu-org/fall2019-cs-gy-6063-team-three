from django.test import TestCase
from django.urls import reverse

from OneApply.constants import UserType
from register.models import Student
from .models import HighSchool


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


def update_session(client, username, user_type=UserType.STUDENT):
    s = client.session
    s.update({"username": username, "is_login": True, "user_type": user_type})
    s.save()


class HighSchoolModelTest(TestCase):
    def create_highschool(self, dbn="06A231"):
        return HighSchool.objects.create(
            dbn=dbn,
            school_name="Testing High School for Bugs!",
            boro="K",
            overview_paragraph="The mission of Testing High School for Bugs is "
            "to intellectually prepare, morally inspire, and socially motivate "
            "every bug to become non-existent in this vastly changing project.",
            neighborhood="Downtown-Brooklyn",
            location="0 MTep Street, Brooklyn NY 00192(01.010101, -02.020202)",
            phone_number="912-121-0911",
            school_email="temp@schools.cyn.vog",
            website="testhighschool.com",
            total_students=5,
            start_time="9am",
            end_time="2pm",
            graduation_rate=".99",
        )

    def test_create_highschool(self):
        high_school = self.create_highschool()
        self.assertEqual(isinstance(high_school, HighSchool), True)
        self.assertEqual(high_school.dbn, "06A231")
        self.assertEqual(high_school.school_name, "Testing High School for Bugs!")
        self.assertEqual(high_school.boro, "K")
        self.assertEqual(
            high_school.overview_paragraph,
            "The mission of Testing High School for Bugs is to intellectually "
            "prepare, morally inspire, and socially motivate every bug to "
            "become non-existent in this vastly changing project.",
        )
        self.assertEqual(high_school.neighborhood, "Downtown-Brooklyn")
        self.assertEqual(
            high_school.location,
            "0 MTep Street, Brooklyn NY 00192(01.010101, " "-02.020202)",
        )
        self.assertEqual(high_school.phone_number, "912-121-0911")
        self.assertEqual(high_school.school_email, "temp@schools.cyn.vog")
        self.assertEqual(high_school.website, "testhighschool.com")
        self.assertEqual(high_school.total_students, 5)
        self.assertEqual(high_school.start_time, "9am")
        self.assertEqual(high_school.end_time, "2pm")
        self.assertEqual(high_school.graduation_rate, ".99")

    def test_get_highschool(self):
        high_school = self.create_highschool()
        response = HighSchool.objects.get(dbn="06A231")
        self.assertTrue(response.dbn, high_school.dbn)

    def test_delete_highschool(self):
        self.create_highschool()
        response = HighSchool.objects.filter(dbn="06A231").delete()
        self.assertIsNotNone(response)


class HighSchoolViewTests(TestCase):
    def create_highschool(self, dbn="06A231", phone_number="912-121-0911"):
        return HighSchool.objects.create(
            dbn=dbn,
            school_name="Testing High School for Bugs!",
            boro="K",
            overview_paragraph="The mission of Testing High School for Bugs is to "
            "intellectually prepare, morally inspire, and socially "
            "motivate every bug to become non-existent in this vastly changing project.",  # noqa: E501
            neighborhood="Downtown-Brooklyn",
            location="0 MTep Street, Brooklyn NY 00192(01.010101, -02.020202)",
            phone_number=phone_number,
            school_email="temp@schools.cyn.vog",
            website="testhighschool.com",
            total_students=5,
            start_time="9am",
            end_time="2pm",
            graduation_rate=".99",
        )

    def test_no_student_login(self):
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_valid_student_login(self):
        self.create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Testing High School for Bugs!")

    def test_invalid_student_login(self):
        update_session(self.client, "studentone", user_type=UserType.ADMIN_STAFF)
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "without proper credentials")

    def test_one_entry(self):
        self.create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "06A231")
        self.assertContains(response, "912-121-0911")

    def test_two_entries(self):
        self.create_highschool()
        self.create_highschool("05A221", "311-911-2100")
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "06A231")
        self.assertContains(response, "05A221")
        self.assertContains(response, "311-911-2100")

    def test_no_entries(self):
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Oops! We couldn't find your high school")
        self.assertContains(
            response, "Contact oneapply_teamthree@gmail.com if the problem persists."
        )

    def test_unauthorized(self):
        # TODO: add appropriate test case
        # for checking unauthorized access to /high_school page
        # and update above test case accordingly to fail if authorized
        pass
