from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from .models import Fruit


def create_fruits(cls):
    cls.blueberry = Fruit.objects.create(name='blueberry', unit_price=300)
    cls.lemon = Fruit.objects.create(name='lemon', unit_price=80)
    cls.apple = Fruit.objects.create(name='apple', unit_price=90)


class FruitModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruits(cls)

    def setUp(self):
        pass

    def test_str(self):
        self.assertEqual(str(self.blueberry), 'blueberry')
        self.assertEqual(str(self.lemon), 'lemon')
        self.assertEqual(str(self.apple), 'apple')


class FruitViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user('tester', password='pass')
        create_fruits(cls)

    def setUp(self):
        self.urls = {
            'list': reverse('products:fruits:list'),
            'add': reverse('products:fruits:add'),
            'edit': self.apple.get_absolute_url(),
            'delete': reverse('products:fruits:delete', args=(self.apple.pk,)),
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
