from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from OneApply.constants import UserType
from register.models import Student, Admin_Staff
from high_school.models import HighSchool
from high_school.tests import update_session


def create_users(just_student=False):
    student_obj = Student.objects.create(
        first_name="John",
        last_name="Doe",
        email_address="john.doe@nothing.com",
        username="j_doe",
        password=make_password("john_doe@10"),
        current_school="NYU",
        borough="MN",
        is_active=True,
    )
    admin_staff_obj = None
    if not just_student:
        high_school_obj = HighSchool.objects.create(
            dbn="06M540",
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

        admin_staff_obj = Admin_Staff.objects.create(
            first_name="John",
            last_name="Doe2",
            email_address="john.doe2@nothing.com",
            username="j_doe2",
            password=make_password("john_doe@20"),
            school=high_school_obj,
            supervisor_email="john.doe3@nothing.com",
            is_verified_employee=True,
            is_active=True,
        )

    return student_obj, admin_staff_obj


class DashboardTests(TestCase):
    def setUp(self):
        self.student, self.admin_staff = create_users()

    def test_student_login(self):
        update_session(self.client, self.student.username, user_type=UserType.STUDENT)
        url = reverse("dashboard:dashboard")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("dashboard:high_school:index"))

    def test_admin_staff_login(self):
        update_session(
            self.client, self.admin_staff.username, user_type=UserType.ADMIN_STAFF
        )
        url = reverse("dashboard:dashboard")
        response = self.client.get(url)
        self.assertRedirects(response, reverse("dashboard:admissions:index"))

    def test_user_logout(self):
        update_session(self.client, self.student.username, user_type=UserType.STUDENT)
        response = self.client.get(reverse("dashboard:logout"))
        self.assertRedirects(response, reverse("landingpage:index"))
        # test invalid access
        response = self.client.get(reverse("dashboard:dashboard"))
        self.assertRedirects(response, reverse("landingpage:index"))
