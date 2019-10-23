from django.test import RequestFactory, TestCase
from django.urls import reverse
from OneApply.constants import *
from register.models import Admin_Staff


class AdmissionStaffTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adminStaff = {'username': 'jwang',
                           'first_name': 'Jenny',
                           'last_name': 'Wang',
                           'email_address': 'jenny.wang@gmail.com',
                           'school': 'NYU',
                           'supervisor_email': 'jack.w@nyu.edu',
                           'input_password': 'Jenny@1234',
                           'confirm_password': 'Jenny@1234'}

    def test_register_admin(self):
        url = reverse('register:register_user',
                      args=[UserType.ADMIN_STAFF])
        response = self.client.post(url,
                                    self.adminStaff)
        # print(Admin_Staff.objects.all())
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        Admin_Staff.objects.all().delete()


class AdmissionStaffModelTest(TestCase):

    def create_admission_staff(self):
        return Admin_Staff.objects.create(username='jwang',
                                          first_name='Jenny',
                                          last_name='Wang',
                                          email_address='jenny.wang@gmail.com',
                                          school='NYU',
                                          supervisor_email='jack.w@nyu.edu',
                                          password='Jenny@1234')

    def test_create_admission(self):
        admissions_staff = self.create_admission_staff()
        self.assertEqual(isinstance(admissions_staff, Admin_Staff), True)
        self.assertEqual(admissions_staff.username, 'jwang')
        self.assertEqual(admissions_staff.first_name, 'Jenny')
        self.assertEqual(admissions_staff.last_name, 'Wang')
        self.assertEqual(admissions_staff.email_address, 'jenny.wang@gmail.com')
        self.assertEqual(admissions_staff.school, 'NYU')
        self.assertEqual(admissions_staff.supervisor_email, 'jack.w@nyu.edu')
        print(Admin_Staff.objects.all())

    def test_get_admission(self):
        admissions_staff = self.create_admission_staff()
        response = Admin_Staff.objects.get(username='jwang')
        self.assertTrue(response.username, admissions_staff.username)

    def test_delete_admission(self):
        self.create_admission_staff()
        response = Admin_Staff.objects.filter(username='jwang').delete()
        self.assertIsNotNone(response)
