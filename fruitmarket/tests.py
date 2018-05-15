from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class AuthViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('tester', password='pass')

    def setUp(self):
        pass

    def test_login_required_at_index(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       reverse('index'))
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_with_authentication(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGIN_REDIRECT_URL))

    def test_logout_with_authentication(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(settings.LOGOUT_REDIRECT_URL))
