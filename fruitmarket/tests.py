import datetime
from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from .core import utils


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


class UtilTests(SimpleTestCase):

    def setUp(self):
        self.today = datetime.date.today()

    def test_to_datetime(self):
        value = utils.to_datetime(self.today)
        self.assertIsInstance(value, datetime.datetime)
        self.assertEqual(value.hour, 0)
        self.assertEqual(value.minute, 0)
        self.assertEqual(value.second, 0)
        self.assertEqual(value.microsecond, 0)
        self.assertEqual(value.tzinfo.zone, settings.TIME_ZONE)

    @override_settings(USE_TZ=False)
    def test_to_datetime_without_tz(self):
        value = utils.to_datetime(self.today)
        self.assertIsInstance(value, datetime.datetime)
        self.assertIsNone(value.tzinfo)

    def test_get_current_month(self):
        month = utils.get_current_month(self.today)
        self.assertEqual(month.day, 1)

    def test_get_next_month(self):
        date = datetime.date(2018, 5, 23)
        next_month = utils.get_next_month(date)
        self.assertEqual(next_month, datetime.date(2018, 6, 1))

    def test_get_next_month_of_december(self):
        date = datetime.date(2018, 12, 23)
        next_month = utils.get_next_month(date)
        self.assertEqual(next_month, datetime.date(2019, 1, 1))

    def test_get_next_month_for_value_error(self):
        date = datetime.date(9999, 12, 23)
        with self.assertRaises(ValueError):
            utils.get_next_month(date)
