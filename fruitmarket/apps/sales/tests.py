import os
import datetime
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from fruitmarket.apps.products.tests import create_fruits
from .models import FruitSales
from .services import FruitSalesStats, FruitSalesSet
from .forms import FruitSalesCSVUploadForm

DIR = os.path.dirname(os.path.abspath(__file__))
VALID_CSV_FNAME = os.path.join(DIR, 'misc/test_valid.csv')
INVALID_CSV_FNAME = os.path.join(DIR, 'misc/test_invalid.txt')
CP932_CSV_FNAME = os.path.join(DIR, 'misc/test_invalid_encoding.csv')


def create_fruitsales(cls):
    create_fruits(cls)
    cls.blueberry_sale = FruitSales.objects.create(fruit=cls.blueberry, quantity=3)
    cls.lemon_sale = FruitSales.objects.create(fruit=cls.lemon, quantity=3)
    cls.apple_sale = FruitSales.objects.create(fruit=cls.apple, quantity=3)
    cls.apple_sale_alt = FruitSales.objects.create(fruit=cls.apple, quantity=2)


class FruitSalesModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)

    def setUp(self):
        pass

    def test_str(self):
        self.assertRegex(str(self.blueberry_sale), r'^%s' % self.blueberry)
        self.assertRegex(str(self.lemon_sale), r'^%s' % self.lemon)
        self.assertRegex(str(self.apple_sale), r'^%s' % self.apple)

    def test_amount(self):
        self.assertEqual(self.blueberry_sale.amount,
                         self.blueberry.unit_price * self.blueberry_sale.quantity)
        self.assertEqual(self.lemon_sale.amount,
                         self.lemon.unit_price * self.lemon_sale.quantity)
        self.assertEqual(self.apple_sale.amount,
                         self.apple.unit_price * self.apple_sale.quantity)

    def test_amount_on_unit_price_changed(self):
        amount = self.blueberry_sale.amount
        self.blueberry.unit_price += 100
        self.blueberry.save()
        self.assertEqual(self.blueberry_sale.amount, amount)

    def test_amount_on_quantity_changed(self):
        amount = self.blueberry_sale.amount
        self.blueberry_sale.quantity += 10
        self.blueberry_sale.save()
        self.assertEqual(self.blueberry_sale.amount, amount)


class FruitSalesManagerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)
        cls.manager = FruitSales.objects
        cls.today = datetime.date.today()

    def setUp(self):
        pass

    def test_gross(self):
        self.assertEqual(self.manager.gross(),
                         sum([self.blueberry_sale.amount,
                              self.lemon_sale.amount,
                              self.apple_sale.amount,
                              self.apple_sale_alt.amount]))

    def test_subtotal_amount(self):
        self.assertEqual(self.manager.filter(fruit=self.apple).total_amount(),
                         sum([self.apple_sale.amount, self.apple_sale_alt.amount]))

    def test_daily(self):
        self.assertEqual(self.manager.daily(self.today).count(),
                         self.manager.count())

    def test_monthly(self):
        self.assertEqual(self.manager.monthly(self.today).count(),
                         self.manager.count())


class FruitSalesServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)
        cls.qs = FruitSales.objects.all()
        cls.stats = FruitSalesStats(cls.qs)

    def setUp(self):
        pass

    def test_total_amount(self):
        self.assertEqual(self.stats.total_amount(), self.qs.total_amount())

    def test_breakdown(self):
        with self.assertNumQueries(0):
            breakdown = self.stats.breakdown()
        with self.assertNumQueries(1):
            for sub in breakdown:
                self.assertIsInstance(sub, FruitSalesSet)


class FruitSalesCSVUploadFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruits(cls)
        cls.form_class = FruitSalesCSVUploadForm

    def setUp(self):
        pass

    def test_get_result_at_first(self):
        form = self.form_class()
        with self.assertRaisesRegex(AssertionError, r'save()'):
            form.imported
        with self.assertRaisesRegex(AssertionError, r'save()'):
            form.ignored
        with self.assertRaisesRegex(AssertionError, r'save()'):
            form.result

    def test_call_save_at_first(self):
        form = self.form_class()
        with self.assertRaisesRegex(AssertionError, r'is_valid()'):
            form.save()

    def test_is_valid_with_empty_data(self):
        form = self.form_class(files={})
        self.assertFalse(form.is_valid())
        with self.assertRaisesRegex(AssertionError, r'invalid'):
            form.save()

    def test_is_valid_with_non_csvfile(self):
        with open(INVALID_CSV_FNAME, 'rb') as f:
            files = {'file_': SimpleUploadedFile(INVALID_CSV_FNAME, f.read(),
                                                 content_type='text/plain')}
        form = self.form_class(files=files)
        self.assertFalse(form.is_valid())
        with self.assertRaisesRegex(AssertionError, r'invalid'):
            form.save()

    def test_is_valid_with_csvfile_encoded_cp932(self):
        with open(CP932_CSV_FNAME, 'rb') as f:
            files = {'file_': SimpleUploadedFile(CP932_CSV_FNAME, f.read(),
                                                 content_type='text/csv')}
        form = self.form_class(files=files)
        self.assertFalse(form.is_valid())
        with self.assertRaisesRegex(AssertionError, r'invalid'):
            form.save()

    def test_csv_upload_form_valid_csvfile(self):
        with open(VALID_CSV_FNAME, 'rb') as f:
            files = {'file_': SimpleUploadedFile(VALID_CSV_FNAME, f.read(),
                                                 content_type='text/csv')}
        form = self.form_class(files=files)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(form.imported), 6)
        self.assertEqual(len(form.ignored), 8)
        self.assertIsInstance(form.result, str)


class FruitSalesViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('tester', password='pass')
        create_fruitsales(cls)

    def setUp(self):
        self.urls = {
            'list': reverse('sales:fruits:list'),
            'add': reverse('sales:fruits:add'),
            'edit': self.apple_sale.get_absolute_url(),
            'delete': reverse('sales:fruits:delete', args=(self.apple_sale.pk,)),
            'stats': reverse('sales:stats:overview'),
            'pandas': reverse('sales:stats:pandas'),
        }

    def test_login_required_at_list(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['list'])
        response = self.client.get(self.urls['list'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_required_at_add(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['add'])
        response = self.client.get(self.urls['add'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_required_at_edit(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['edit'])
        response = self.client.get(self.urls['edit'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_required_at_delete(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['delete'])
        response = self.client.get(self.urls['delete'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_required_at_stats(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['stats'])
        response = self.client.get(self.urls['stats'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_login_required_at_pandas(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['pandas'])
        response = self.client.get(self.urls['pandas'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_stats(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('sales/fruitsales_stats.html'):
            response = self.client.get(self.urls['stats'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['gross'], FruitSales.objects.gross())

    def test_pandas(self):
        self.client.force_login(self.user)
        with self.assertTemplateUsed('sales/fruitsales_dataframe_stats.html'):
            response = self.client.get(self.urls['pandas'])
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['stats'].gross, FruitSales.objects.gross())

    def test_post_csv_upload_without_auth(self):
        expected_url = '%s?next=%s' % (reverse(settings.LOGIN_URL),
                                       self.urls['list'])
        response = self.client.post(self.urls['list'])
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url)

    def test_post_csv_upload_without_data(self):
        self.client.force_login(self.user)
        response = self.client.post(self.urls['list'])
        self.assertEqual(response.status_code, 200)
        self.assertIn('file_', response.context['form'].errors)

    def test_post_csv_upload_with_valid_data(self):
        self.client.force_login(self.user)
        with open(VALID_CSV_FNAME, 'rb') as f:
            response = self.client.post(self.urls['list'], {'file_': f}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(response.redirect_chain, [(self.urls['list'], 302)])
        self.assertGreaterEqual(len(response.context['messages']), 1)
