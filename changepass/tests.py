from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.apps import apps
from .apps import ChangepassConfig
from OneApply.constants import UserType
from .forms import changepassForm, resetPassFormStudent, resetPassFormAdmin
from register.models import Student, Admin_Staff
from high_school.models import HighSchool


def update_session_student(client, user):
    s = client.session
    s.update(
        {"username": user.username, "is_login": True, "user_type": UserType.STUDENT}
    )
    s.save()


def update_session_admin(client, user):
    a = client.session
    a.update(
        {"username": user.username, "is_login": True, "user_type": UserType.ADMIN_STAFF}
    )
    a.save()


class ChangePassFormTest(TestCase):
    def test_change_form_valid(self):
        data = {
            "old_password": "Jenny@1234",
            "new_password": "Jenny@0987",
            "confirm_password": "Jenny@0987",
        }
        form = changepassForm(data=data)
        self.assertTrue(form.is_valid())

    def test_change_form_invalid_password(self):
        data = {
            "old_password": "Jenny@1234",
            "new_password": "Jenny0987",
            "confirm_password": "Jenny0987",
        }
        form = changepassForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("new_password" in form.cleaned_data)

    def test_change_form_mismatch_password(self):
        data = {
            "old_password": "Jenny@1234",
            "new_password": "Jenny@0987",
            "confirm_password": "Jenny@@0987",
        }
        form = changepassForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("confirm_password" in form.cleaned_data)


class ResetPassFormStudentTest(TestCase):
    def create_student(self):
        return Student.objects.create(
            first_name="Hritik",
            last_name="Roshan",
            email_address="fake@email.com",
            username="hritik",
            password="hritikRoshan@10",
            current_school="NYU",
            borough="MN",
        )

    def setUp(self):
        self.student = self.create_student()

    def test_reset_student_form_valid(self):
        data = {"email_address": "fake@email.com"}
        form = resetPassFormStudent(data=data)
        self.assertTrue(form.is_valid())

    def test_reset_student_form_invalid_email(self):
        data = {"email_address": "fakeemail.com"}
        form = resetPassFormStudent(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("email_address" in form.cleaned_data)

    def test_reset_student_form_email_no_account(self):
        data = {"email_address": "fake3@email.com"}
        form = resetPassFormStudent(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("email_address" in form.cleaned_data)

    def tearDown(self):
        self.student.delete()


class ResetPassFormAdminTest(TestCase):
    def create_admission_staff(self):
        hs = HighSchool.objects.create(
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
        return Admin_Staff.objects.create(
            username="jwang",
            first_name="Jenny",
            last_name="Wang",
            email_address="jenny.wang@gmail.com",
            school=hs,
            supervisor_email="jack.w@nyu.edu",
            password="Jenny@1234",
        )

    def setUp(self):
        self.admission_staff = self.create_admission_staff()

    def test_reset_admin_form_valid(self):
        data = {"email_address": "jenny.wang@gmail.com"}
        form = resetPassFormAdmin(data=data)
        self.assertTrue(form.is_valid())

    def test_reset_admin_form_invalid_email(self):
        data = {"email_address": "fakeemail.com"}
        form = resetPassFormAdmin(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("email_address" in form.cleaned_data)

    def test_reset_admin_form_email_no_account(self):
        data = {"email_address": "fake3@email.com"}
        form = resetPassFormAdmin(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("email_address" in form.cleaned_data)

    def tearDown(self):
        self.admission_staff.delete()


class ResetPassViewTest(TestCase):
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

    def create_admission_staff(self):
        hs = HighSchool.objects.create(
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
        return Admin_Staff.objects.create(
            username="jwang",
            first_name="Jenny",
            last_name="Wang",
            email_address="jenny.wang@gmail.com",
            school=hs,
            supervisor_email="jack.w@nyu.edu",
            password="Jenny@1234",
        )

    def setUp(self):
        self.student = self.create_student()
        self.admission_staff = self.create_admission_staff()

    def test_valid_student_reset(self):
        data = {"email_address": "hrx@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_student_reset(self):
        data = {"email_address": "hrx1234@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_not_post_student_reset(self):
        data = {"email_address": "hrx1234@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.STUDENT])
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_valid_admin_reset(self):
        data = {"email_address": "jenny.wang@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_admin_reset(self):
        data = {"email_address": "jenny.wang22@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_not_post_admin_reset(self):
        data = {"email_address": "jenny.wang22@gmail.com"}
        url = reverse("changepass:reset_password", args=[UserType.ADMIN_STAFF])
        response = self.client.get(url, data=data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.student.delete()
        self.admission_staff.delete()


class ChangePassConfigTest(TestCase):
    def test_apps(self):
        self.assertEqual(ChangepassConfig.name, "changepass")
        self.assertEqual(apps.get_app_config("changepass").name, "changepass")


class IndexViewTest(TestCase):
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

    def create_admission_staff(self):
        hs = HighSchool.objects.create(
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
        return Admin_Staff.objects.create(
            username="jwang",
            first_name="Jenny",
            last_name="Wang",
            email_address="jenny.wang@gmail.com",
            school=hs,
            supervisor_email="jack.w@nyu.edu",
            password=make_password("Jenny@1234"),
        )

    def setUp(self):
        self.student = self.create_student()
        self.admission_staff = self.create_admission_staff()

    def test_no_login(self):
        url = reverse("changepass:index")
        response = self.client.get(url)
        self.assertTrue(response.status_code, 302)

    def test_valid_student_change(self):
        update_session_student(self.client, self.student)
        data = {
            "old_password": "hritikRoshan@10",
            "new_password": "hritikRoshan@11",
            "confirm_password": "hritikRoshan@11",
        }
        url = reverse("changepass:index")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_student_change(self):
        update_session_student(self.client, self.student)
        data = {
            "old_password": "hritikRoshan@9",
            "new_password": "hritikRoshan@11",
            "confirm_password": "hritikRoshan@11",
        }
        url = reverse("changepass:index")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def test_valid_admin_change(self):
        update_session_admin(self.client, self.admission_staff)
        data = {
            "old_password": "Jenny@1234",
            "new_password": "hritikRoshan@11",
            "confirm_password": "hritikRoshan@11",
        }
        url = reverse("changepass:index")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_invalid_admin_change(self):
        update_session_admin(self.client, self.admission_staff)
        data = {
            "old_password": "Jenny@14",
            "new_password": "hritikRoshan@11",
            "confirm_password": "hritikRoshan@11",
        }
        url = reverse("changepass:index")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.student.delete()
        self.admission_staff.delete()
