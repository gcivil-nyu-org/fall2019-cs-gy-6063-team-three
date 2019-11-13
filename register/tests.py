from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from OneApply.constants import UserType
from high_school.models import HighSchool
from .forms import StudentRegisterForm, AdminStaffRegisterForm
from .models import Student, Admin_Staff
from .tokens import account_activation_token


class AdmissionStaffViewTest(TestCase):
    def create_school(self):
        return HighSchool.objects.create(
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

    def setUp(self):
        self.create_school()
        self.adminStaff = {
            "username": "jwang",
            "first_name": "Jenny",
            "last_name": "Wang",
            "email_address": "jenny.wang@gmail.com",
            "supervisor_email": "jack.w@nyu.edu",
            "input_password": "Jenny@1234",
            "confirm_password": "Jenny@1234",
        }

    def test_valid_register_admin(self):
        url = reverse("register:register_user", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, self.adminStaff)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Admin_Staff.objects.get(username="jwang"))

    def test_invalid_register_admin(self):
        self.adminStaff = {
            "username": "JWANG",
            "first_name": "Jenny",
            "last_name": "Wang",
            "email_address": "jenny.wang@gmail.com",
            "supervisor_email": "jack.w@nyu.edu",
            "input_password": "Jenny@1234",
            "confirm_password": "Jenny@1234",
        }
        url = reverse("register:register_user", args=[UserType.ADMIN_STAFF])
        response = self.client.post(url, self.adminStaff)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Admin_Staff.objects.filter(username="jwang").count(), 0)

    def tearDown(self):
        Admin_Staff.objects.all().delete()


class AdmissionStaffModelTest(TestCase):
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
            is_active=True,
        )

    def test_create_admission(self):
        admissions_staff = self.create_admission_staff()
        self.assertEqual(isinstance(admissions_staff, Admin_Staff), True)
        self.assertEqual(admissions_staff.username, "jwang")
        self.assertEqual(admissions_staff.first_name, "Jenny")
        self.assertEqual(admissions_staff.last_name, "Wang")
        self.assertEqual(admissions_staff.email_address, "jenny.wang@gmail.com")
        self.assertEqual(admissions_staff.supervisor_email, "jack.w@nyu.edu")

    def test_get_admission(self):
        admissions_staff = self.create_admission_staff()
        response = Admin_Staff.objects.get(username="jwang")
        self.assertTrue(response.username, admissions_staff.username)

    def test_delete_admission(self):
        self.create_admission_staff()
        response = Admin_Staff.objects.filter(username="jwang").delete()
        self.assertIsNotNone(response)


class AdmissionsFormTest(TestCase):
    def test_admission_staff_valid_form(self):
        data = {
            "username": "jwang",
            "first_name": "Jenny",
            "last_name": "Wang",
            "email_address": "jenny.wang@gmail.com",
            "supervisor_email": "jack.w@nyu.edu",
            "input_password": "Jenny@1234",
            "confirm_password": "Jenny@1234",
        }
        form = AdminStaffRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_admission_staff_invalid_password(self):
        data = {
            "username": "jwang",
            "first_name": "Jenny",
            "last_name": "Wang",
            "email_address": "jenny.wang@gmail.com",
            "supervisor_email": "jack.w@nyu.edu",
            "input_password": "Jenny1234",
            "confirm_password": "Jenny1234",
        }
        form = AdminStaffRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("input_password" in form.cleaned_data)

    def test_admission_staff_mismatch_password(self):
        data = {
            "username": "jwang",
            "first_name": "Jenny",
            "last_name": "Wang",
            "email_address": "jenny.wang@gmail.com",
            "supervisor_email": "jack.w@nyu.edu",
            "input_password": "Jenny@1234",
            "confirm_password": "Jenny@1234567",
        }
        form = AdminStaffRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("confirm_password" in form.cleaned_data)


class AdmissionsViewActivateTest(TestCase):
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

    def test_verification_admission_staff(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.admission_staff.pk))
        token = account_activation_token.make_token(self.admission_staff)
        url = reverse("verify_employee_status", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_id_verification_admission_staff(self):
        uid64 = urlsafe_base64_encode(force_bytes(1000000))
        token = account_activation_token.make_token(self.admission_staff)
        url = reverse("verify_employee_status", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_verification_admission_staff(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.admission_staff.pk))
        token = account_activation_token.make_token(self.admission_staff)
        token = token[:-3]
        token += "xyz"
        url = reverse("verify_employee_status", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_activation_admission_staff(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.admission_staff.pk))
        token = account_activation_token.make_token(self.admission_staff)
        url = reverse("activate_admission_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_id_activation_admission_staff(self):
        uid64 = urlsafe_base64_encode(force_bytes(10000000))
        token = account_activation_token.make_token(self.admission_staff)
        url = reverse("activate_admission_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_activation_student(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.admission_staff.pk))
        token = account_activation_token.make_token(self.admission_staff)
        token = token[:-3]
        token += "xyz"
        url = reverse("activate_admission_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.admission_staff.delete()


class StudentModelTest(TestCase):
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

    def test_create(self):
        student = self.create_student()
        self.assertTrue(isinstance(student, Student))
        self.assertEqual(student.email_address, "hrx@gmail.com")
        self.assertEqual(student.username, "hritik")
        self.assertEqual(student.password, "hritikRoshan@10")

    def test_get(self):
        student = self.create_student()
        response = Student.objects.get(username="hritik")
        self.assertTrue(response.username, student.username)

    def test_delete(self):
        self.create_student()
        response = Student.objects.filter(username="hritik").delete()
        self.assertIsNotNone(response)


class StudentFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@10",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikroshan@",
            "confirm_password": "hritikroshan@",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("input_password" in form.cleaned_data)

    def test_mismatch_password(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@1",
            "current_school": "NYU",
            "borough": "MN",
        }
        form = StudentRegisterForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFalse("confirm_password" in form.cleaned_data)


class StudentViewTest(TestCase):
    def test_valid_register_student(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@10",
            "current_school": "NYU",
            "borough": "MN",
        }
        url = reverse("register:register_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Student.objects.get(username="hritik"))

    def test_invalid_register_student(self):
        data = {
            "first_name": "Hritik",
            "last_name": "Roshan",
            "email_address": "hrx@gmail.com",
            "phoneNumber": "9567801234",
            "username": "hritik",
            "input_password": "hritikRoshan@10",
            "confirm_password": "hritikRoshan@575",
            "current_school": "NYU",
            "borough": "MN",
        }
        url = reverse("register:register_user", args=[UserType.STUDENT])
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Student.objects.filter(username="hritik").count(), 0)


class StudentViewActivateTest(TestCase):
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

    def setUp(self):
        self.student = self.create_student()

    def test_activation_student(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.student.pk))
        token = account_activation_token.make_token(self.student)
        url = reverse("activate_student_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_id_activation_student(self):
        uid64 = urlsafe_base64_encode(force_bytes(10000000))
        token = account_activation_token.make_token(self.student)
        url = reverse("activate_student_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def test_invalid_token_activation_student(self):
        uid64 = urlsafe_base64_encode(force_bytes(self.student.pk))
        token = account_activation_token.make_token(self.student)
        token = token[:-3]
        token += "xyz"
        url = reverse("activate_student_account", args=[uid64, token])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.student.delete()
