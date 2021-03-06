from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from OneApply.constants import UserType
from register.models import Student, Admin_Staff
from .forms import SaveHighSchoolsForm
from .models import HighSchool, Program
from .templatetags import hs_filters as filters


def create_highschool(
    dbn="06A231",
    school_name="Testing High School for Bugs!",
    phone_number="912-121-0911",
    boro="K",
    location="0 MTep Street, Brooklyn NY 00192(01.010101, -02.020202)",
):
    return HighSchool.objects.create(
        dbn=dbn,
        school_name=school_name,
        boro=boro,
        overview_paragraph="The mission of Testing High School for Bugs is to "
        "intellectually prepare, morally inspire, and socially "
        "motivate every bug to become non-existent in this "
        "vastly changing project.",  # noqa: E501
        neighborhood="Downtown-Brooklyn",
        location=location,
        phone_number=phone_number,
        school_email="temp@schools.cyn.vog",
        website="testhighschool.com",
        total_students=5,
        start_time="9am",
        end_time="2pm",
        graduation_rate=".99",
    )


def create_student(user_name="studentone", last_name="Doe"):
    return Student.objects.create(
        username=user_name,
        first_name="John",
        last_name="Doe",
        email_address="john.doe@gmail.com",
        current_school="NYU",
        borough="B",
        password="Something@123",
    )


def create_program(code="Q83C", high_school=None, name="Academy of Engineering"):
    if not high_school:
        high_school = create_highschool("06A231", phone_number="912-121-0911")
    return Program.objects.create(
        high_school=high_school,
        name=name,
        code=code,
        description="New York State approved CTE Program that leads to national "
        "certification aligned with industry standards and a "
        "CTE-endorsed Regents Diploma. Interdisciplinary "
        "project-based curriculum includes coursework in Introduction "
        "to Engineering & Design, Digital Electronics, Principles of "
        "Engineering, and Engineering Design & Development.",
        number_of_seats=70,
        offer_rate=0,
    )


def update_session(client, username, is_login=True, user_type=UserType.STUDENT):
    s = client.session
    s.update({"username": username, "is_login": is_login, "user_type": user_type})
    s.save()


class HighSchoolModelTest(TestCase):
    def test_create_highschool(self):
        high_school = create_highschool()
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
        high_school = create_highschool()
        response = HighSchool.objects.get(dbn="06A231")
        self.assertTrue(response.dbn, high_school.dbn)

    def test_delete_highschool(self):
        create_highschool()
        response = HighSchool.objects.filter(dbn="06A231").delete()
        self.assertIsNotNone(response)


class HighSchoolViewTests(TestCase):
    def setUp(self):
        create_student()

    def test_no_login(self):
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertTrue(response.status_code, 302)

    def test_no_student_login(self):
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_valid_student_login(self):
        create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Testing High School for Bugs!")

    def test_invalid_student_login(self):
        hs = create_highschool()
        # test invalid user type
        Admin_Staff.objects.create(
            first_name="Hritik",
            last_name="Roshan",
            email_address="hrx@gmail.com",
            username="hritik",
            password="hritikRoshan@10",
            school=hs,
            supervisor_email="hrx@gmail.com",
            is_verified_employee=True,
            is_active=True,
        )
        update_session(self.client, "adminstaff_one", user_type=UserType.ADMIN_STAFF)
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        # updated for redirection to login if user invalid
        self.assertEquals(response.status_code, 302)
        # test student object does not exist
        update_session(self.client, "student_two", user_type=UserType.STUDENT)
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        # updated for redirection to login if user invalid
        self.assertEquals(response.status_code, 302)

    def test_one_entry(self):
        create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "06A231")
        self.assertContains(response, "912-121-0911")

    def test_two_entries(self):
        create_highschool()
        create_highschool("05A221", "311-911-2100")
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
            create_highschool(dbn="12A0" + str(hs_dbn))

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
        self.assertTrue(
            "empty_list" in response.context and response.context["empty_list"] == 1
        )
        self.assertContains(response, "Oops! We couldn't find what you're looking for")
        self.assertContains(
            response, "Contact oneapply_teamthree@gmail.com if the problem persists."
        )

    def test_selected_highschool(self):
        create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:overview", args=["06A231"])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue("selected_school" in response.context)
        self.assertContains(response, "Testing High School for Bugs!")
        self.assertContains(response, "0 MTep Street, Brooklyn NY 00192")
        self.assertContains(response, "912-121-0911")

    def test_selected_school_empty(self):
        create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:overview", args=["06ACP9"])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue("selected_school" in response.context)
        self.assertFalse(response.context["selected_school"])
        self.assertTrue("empty_list" in response.context)
        self.assertTrue(response.context["empty_list"], 1)

    def test_selected_school_programs_empty(self):
        # test empty programs
        create_highschool()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:overview", args=["06A231"])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue("selected_school" in response.context)
        self.assertTrue("selected_school_programs" in response.context)
        self.assertFalse(response.context["selected_school_programs"])
        self.assertContains(response, "No programs available")

    def test_selected_school_programs(self):
        # test non empty programs
        create_program()
        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:overview", args=["06A231"])
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue("selected_school" in response.context)
        self.assertTrue("selected_school_programs" in response.context)
        self.assertTrue(len(response.context["selected_school_programs"]), 1)
        self.assertContains(response, "Programs available (1)")
        self.assertContains(response, "Q83C")

    def test_filters(self):
        # Create 8 high_schools for search and filter tests
        number_of_hs = 10
        for hs_dbn in range(number_of_hs):
            if hs_dbn < 2:
                high_school = create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="The Bronx" + str(hs_dbn),
                    boro="X",
                    location="Bronx 10451",
                )
                create_program(
                    code="12A0" + str(hs_dbn) + "_P" + str(hs_dbn),
                    high_school=high_school,
                    name="Arts " + str(hs_dbn),
                )
            elif hs_dbn < 4:
                high_school = create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Brooklyn" + str(hs_dbn),
                    boro="K",
                    location="Brooklyn 11238",
                )
                create_program(
                    code="12A0" + str(hs_dbn) + "_P" + str(hs_dbn),
                    high_school=high_school,
                    name="Computer Science " + str(hs_dbn),
                )
            elif hs_dbn < 6:
                high_school = create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Manhattan" + str(hs_dbn),
                    boro="M",
                    location="Manhattan 10010",
                )
                create_program(
                    code="12A0" + str(hs_dbn) + "_P" + str(hs_dbn),
                    high_school=high_school,
                    name="Humanities " + str(hs_dbn),
                )
            elif hs_dbn < 8:
                high_school = create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Queens" + str(hs_dbn),
                    boro="Q",
                    location="Queens 11427",
                )
                create_program(
                    code="12A0" + str(hs_dbn) + "_P" + str(hs_dbn),
                    high_school=high_school,
                    name="Social Sciences" + str(hs_dbn),
                )
            elif hs_dbn < 10:
                high_school = create_highschool(
                    dbn="12A0" + str(hs_dbn),
                    school_name="Staten Island" + str(hs_dbn),
                    boro="R",
                    location="Staten Island 10314",
                )
                create_program(
                    code="12A0" + str(hs_dbn) + "_P" + str(hs_dbn),
                    high_school=high_school,
                    name="Physical Education " + str(hs_dbn),
                )

        update_session(self.client, "studentone")
        url = reverse("dashboard:high_school:index")
        # without any filters - by default "all" filter selected
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 5)  # paginate_by = 5
        self.assertTrue("search_filter_params" in response.context)
        self.assertTrue(
            "loc_all" in response.context["search_filter_params"]["borough"]
        )
        self.assertTrue(response.context["search_filter_params"]["filter_count"], 1)
        # explicit selection of "all" filter
        response = self.client.get(url + "?loc_all=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 5)
        self.assertTrue(response.context["search_filter_params"]["filter_count"], 1)
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
        # search and borough filters (will only return Brooklyn, not Bronx)
        response = self.client.get(url + "?query=Br&loc_bk=on")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("Brooklyn" in school.school_name)
            self.assertFalse("The Bronx" in school.school_name)
        # search using location
        response = self.client.get(url + "?query=10010")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)
        for school in response.context["high_schools"]:
            self.assertTrue("10010" in school.location)
            self.assertFalse("11238" in school.location)
        # search using program
        response = self.client.get(url + "?query=Computer")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]) == 2)


class FavHighSchoolTests(TestCase):
    def setUp(self):
        self.student1 = create_student(user_name="student1", last_name="Doe1")
        self.hs_1 = create_highschool(dbn="06A001", school_name="School 1")
        update_session(self.client, "student1")

    def test_empty_fav(self):
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url + "?is_fav_on=1")
        self.assertEquals(response.status_code, 200)
        self.assertTrue(
            "empty_list" in response.context and response.context["empty_list"] == 2
        )
        self.assertContains(
            response,
            "Use the heart icon to add/remove a high school from your favorites.",
        )
        self.assertContains(
            response, "Contact oneapply_teamthree@gmail.com for more assistance."
        )

    def test_toggle_fav_model(self):
        hs_2 = create_highschool(dbn="06A002")
        hs_3 = create_highschool(dbn="06A003")
        # test adding High School relations for man2many field in Student model
        self.student1.fav_schools.add(self.hs_1)
        self.student1.save()
        relations = self.student1.fav_schools.all()
        self.assertTrue(relations.count(), 1)
        self.assertTrue(self.hs_1 in relations)
        self.student1.fav_schools.add(hs_2)
        self.student1.fav_schools.remove(self.hs_1)
        self.student1.save()
        relations = self.student1.fav_schools.all()
        self.assertFalse(self.hs_1 in relations)
        self.student1.fav_schools.add(hs_3)
        self.student1.save()
        relations = self.student1.fav_schools.all()
        self.assertTrue(relations.count(), 2)

    def test_toggle_fav_api_view(self):
        # test toggle fav add url
        url = reverse("dashboard:high_school:toggle_fav", args=[self.hs_1.dbn, 1])
        response = self.client.post(url).data
        # print(response.content)
        # print(response.data)
        self.assertTrue(response["status"], 200)
        self.assertTrue(response["message"], "Success")
        # test single fav entry
        relations = self.student1.fav_schools.all()
        self.assertTrue(relations.count(), 1)
        url = reverse("dashboard:high_school:index")
        response = self.client.get(url + "?is_fav_on=1")
        self.assertTrue(response.status_code, 200)
        self.assertTrue(len(response.context["high_schools"]), 1)
        self.assertContains(response, "School 1")
        # test toggle fav remove url
        url = reverse("dashboard:high_school:toggle_fav", args=[self.hs_1.dbn, 0])
        response = self.client.post(url).data
        self.assertTrue(response["status"], 200)
        self.assertTrue(response["message"], "Success")
        # removing from model and empty list in view already tested above
        # test invalid high school dbn has no effect on model and view
        url = reverse("dashboard:high_school:toggle_fav", args=["0X181C", 1])
        response = self.client.post(url).data
        self.assertTrue(response["status"], 404)
        self.assertTrue(response["message"], "No matching high school found")
        relations = self.student1.fav_schools.all()
        self.assertFalse(relations.count())
        # test invalid user access
        update_session(self.client, "student2")
        url = reverse("dashboard:high_school:toggle_fav", args=[self.hs_1.dbn, 1])
        response = self.client.post(url).data
        self.assertTrue(response["status"], 403)
        self.assertTrue(response["message"], "Forbidden - invalid user")
        # test invalid method access for api
        response = self.client.get(url)
        self.assertTrue(response.status_code, 405)


class SaveHighSchoolTests(TestCase):
    def test_valid_data(self):
        data = {"limit": 1}
        form = SaveHighSchoolsForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertTrue("limit" in form.cleaned_data)

    def test_invalid_data(self):
        # test blank data
        form = SaveHighSchoolsForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"limit": ["This field is required."]})

        # test invalid data
        form = SaveHighSchoolsForm({"limit": -1})
        self.assertFalse(form.is_valid())
        self.assertTrue(
            form.errors, {"limit": ["Value must be greater than or equal to 1."]}
        )


class ProgramModelTest(TestCase):
    def test_create_program(self):
        program = create_program()
        self.assertEqual(isinstance(program, Program), True)
        self.assertEqual(program.code, "Q83C")
        self.assertEqual(program.name, "Academy of Engineering")
        self.assertEqual(program.number_of_seats, 70)
        self.assertEqual(program.offer_rate, 0)
        self.assertEqual(
            program.description,
            "New York State approved CTE Program that leads to national "
            "certification aligned with industry standards and a "
            "CTE-endorsed Regents Diploma. Interdisciplinary "
            "project-based curriculum includes coursework in Introduction "
            "to Engineering & Design, Digital Electronics, Principles of "
            "Engineering, and Engineering Design & Development.",
        )

    def test_get_program(self):
        program = create_program()
        response = Program.objects.get(code="Q83C")
        self.assertTrue(response.code, program.code)

    def test_delete_program(self):
        create_program()
        response = Program.objects.filter(code="Q83C").delete()
        self.assertIsNotNone(response)


class HSFiltersTest(TestCase):
    def test_split_string(self):
        val = "str&test"
        arg = "&"
        response = filters.split_string(val, arg)
        self.assertTrue(len(response), 2)
        self.assertTrue("str", response[0])
        self.assertTrue("test", response[1])
        # test non occurrence
        arg = "%"
        response = filters.split_string(val, arg)
        self.assertFalse(response)

    def test_req_params(self):
        val = "http://oneapply.com/dashboard/all_schools/?query=q1&loc_bx=on&page=2"
        response = filters.get_req_params(val)
        self.assertTrue(len(response), 3)
        self.assertTrue("query" in response)
        self.assertTrue("loc_bx" in response)
        self.assertTrue("page" in response)
        # test empty param
        val = "http://oneapply.com/dashboard/all_schools/?query=&loc_bx=on&page=2"
        response = filters.get_req_params(val)
        self.assertTrue(len(response), 2)
        self.assertFalse("query" in response)
        # test empty single param
        val = "http://oneapply.com/dashboard/all_schools/?query="
        response = filters.get_req_params(val)
        self.assertFalse(response)

    def test_querystring(self):
        # test invalid input
        val = "http://oneapply.com/dashboard/all_schools"
        arg = ""
        response = filters.get_querystring(val, arg)
        self.assertFalse(response)
        # test adding a param
        val = "http://oneapply.com/dashboard/all_schools"
        arg = "query"
        response = filters.get_querystring(val, arg)
        self.assertTrue("?query" in response)
        # test updating params (when params exist)
        val = "http://oneapply.com/dashboard/all_schools/?query=q1&loc_bx=on&&page=2"
        arg = "page"
        response = filters.get_querystring(val, arg)
        self.assertTrue(
            "?query" in response and "&loc_bx" in response and "&page" in response
        )
        # test updating params (only the same param exist)
        val = "http://oneapply.com/dashboard/all_schools/?page=2"
        arg = "page"
        response = filters.get_querystring(val, arg)
        self.assertTrue("?page" in response)


class ApiCallTests(TestCase):
    def setUp(self):
        # self.hs_admin = HighSchoolAdmin(model=HighSchool, admin_site=AdminSite())
        self.super_user = User.objects.create_superuser(
            username="super", email="super@email.org", password="pass"
        )

        self.client.login(username="super", password="pass")

    def test_valid_api_call(self):
        # assert empty objects
        url = reverse("admin:save_high_schools")
        response = self.client.get(url)
        self.assertTrue(response.status_code, 200)
        self.assertFalse(HighSchool.objects.count())
        self.assertFalse(Program.objects.count())
        # get 1 object from api
        data = {"limit": 1}
        response = self.client.post(url, data=data)
        self.assertTrue(response.status_code, 200)
        high_schools = HighSchool.objects.get_queryset()
        self.assertTrue(len(high_schools), 1)
        self.assertTrue(Program.objects.filter(high_school=high_schools.first()))
        self.assertFalse(response.context["errors"])
        # assert HS duplicate key
        response = self.client.post(url, data=data)
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response.context["response"], "Errors")
