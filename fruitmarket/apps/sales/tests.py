from django.test import TestCase
from fruitmarket.apps.products.tests import create_fruits
from .models import FruitSales


class FruitSalesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruits(cls)
        cls.blueberry_sale = FruitSales.objects.create(fruit=cls.blueberry,
                                                       quantity=3)
        cls.lemon_sale = FruitSales.objects.create(fruit=cls.lemon, quantity=3)
        cls.apple_sale = FruitSales.objects.create(fruit=cls.apple, quantity=3)

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
