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
    def create_highschool(
        self,
        dbn="06A231",
        school_name="Testing High School for Bugs!",
        phone_number="912-121-0911",
        boro="K",
    ):
        return HighSchool.objects.create(
            dbn=dbn,
            school_name=school_name,
            boro=boro,
            overview_paragraph="The mission of Testing High School for Bugs is to "
            "intellectually prepare, morally inspire, and socially "
            "motivate every bug to become non-existent in this vastly "
            "changing project.",
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
        self.assertTrue("unauth" in response.context)
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

    def test_multiple_entries(self):
        # Create 8 high_schools for pagination tests
        number_of_hs = 8
        for hs_dbn in range(number_of_hs):
            self.create_highschool(dbn="12A0" + str(hs_dbn))

        # testing pagination - page 1 should have 5 entries, since paginated_by = 5
        update_session(self.client, "studentone")
        response = self.client.get(reverse("dashboard:high_school:index"))
        self.assertEquals(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["high_schools"]) == 5)

        # testing pagination - page 2 should have the remaining 3 entries
        response = self.client.get(reverse("dashboard:high_school:index") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] is True)
        self.assertTrue(len(response.context["high_schools"]) == 3)

    def test_no_entries(self):
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue("empty_list" in response.context)
        self.assertContains(response, "Oops! We couldn't find what you're looking for")
        self.assertContains(
            response, "Contact oneapply_teamthree@gmail.com if the problem persists."
        )

    def test_selected_highschool(self):
        self.create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:overview", args=["06A231"])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue("selected_school" in response.context)
        self.assertContains(response, "Testing High School for Bugs!")
        self.assertContains(response, "0 MTep Street, Brooklyn NY 00192")
        self.assertContains(response, "912-121-0911")

    def test_filters(self):
        # Create 8 high_schools for search and filter tests
        number_of_hs = 10
        for hs_dbn in range(number_of_hs):
            if hs_dbn < 2:
                self.create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="The Bronx" + str(hs_dbn),
                    boro="X",
                )
            elif hs_dbn < 4:
                self.create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Brooklyn" + str(hs_dbn),
                    boro="K",
                )
            elif hs_dbn < 6:
                self.create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Manhattan" + str(hs_dbn),
                    boro="M",
                )
            elif hs_dbn < 8:
                self.create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Queens" + str(hs_dbn),
                    boro="Q",
                )
            elif hs_dbn < 10:
                self.create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Staten Island" + str(hs_dbn),
                    boro="R",
                )

        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        # without any filters
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 5)  # paginate_by = 5
        # select bronx filter
        response = self.client.get(url + "?loc_bx=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("The Bronx" in school.school_name)
            self.assertFalse("Brooklyn" in school.school_name)
        # select brooklyn filter
        response = self.client.get(url + "?loc_bk=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("Brooklyn" in school.school_name)
            self.assertFalse("Manhattan" in school.school_name)
        # select manhattan filter
        response = self.client.get(url + "?loc_mn=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("Manhattan" in school.school_name)
            self.assertFalse("Queens" in school.school_name)
        # select queens filter
        response = self.client.get(url + "?loc_qn=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("Queens" in school.school_name)
            self.assertFalse("Staten Island" in school.school_name)
        # select staten island filter
        response = self.client.get(url + "?loc_si=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("Staten Island" in school.school_name)
            self.assertFalse("The Bronx" in school.school_name)
        # search should return both The Bronx, and Brooklyn HS
        response = self.client.get(url + "?query=Br")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 4)
        for school in response.context["high_schools"]:
            self.assertTrue(
                "Brooklyn" in school.school_name or "The Bronx" in school.school_name
            )
            self.assertFalse("Manhattan" in school.school_name)
        # search should return none
        response = self.client.get(url + "?query=Long Island")
        self.assertTrue(response.status_code, 200)
        self.assertTrue("empty_list" in response.context)
