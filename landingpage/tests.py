from django.test import TestCase
from django.urls import reverse

from OneApply.constants import UserType
from high_school.tests import update_session
from dashboard.tests import create_users


class LandingPageTests(TestCase):
    def setUp(self):
        self.student_user, _ = create_users(just_student=True)

    def test_session_redirection(self):
        update_session(
            self.client, self.student_user.username, user_type=UserType.STUDENT
        )
        response = self.client.get(reverse("landingpage:index"))
        # dashboard further redirects to specific user type page
        self.assertRedirects(
            response, reverse("dashboard:dashboard"), target_status_code=302
        )
