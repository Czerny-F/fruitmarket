from django.test import TestCase
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
