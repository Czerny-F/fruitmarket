from django.test import TestCase
from django.urls import reverse
from fruitmarket.apps.products.tests import create_fruits
from .models import FruitSales
from .services import FruitSalesStats, FruitSalesSet


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


class FruitSalesManagerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)
        cls.manager = FruitSales.objects

    def setUp(self):
        pass

    def test_gross(self):
        self.assertEqual(self.manager.gross(),
                         sum([self.blueberry_sale.amount,
                              self.lemon_sale.amount,
                              self.apple_sale.amount,
                              self.apple_sale_alt.amount]))

    def test_subtotal(self):
        self.assertEqual(self.manager.filter(fruit=self.apple).total(),
                         sum([self.apple_sale.amount, self.apple_sale_alt.amount]))


class FruitSalesServiceTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)
        cls.qs = FruitSales.objects.all()
        cls.stats = FruitSalesStats(cls.qs)

    def setUp(self):
        pass

    def test_total(self):
        self.assertEqual(self.stats.total, self.qs.total())

    def test_breakdown(self):
        with self.assertNumQueries(0):
            breakdown = self.stats.breakdown()
        with self.assertNumQueries(2):
            for sub in breakdown:
                self.assertIsInstance(sub, FruitSalesSet)


class FruitSalesViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_fruitsales(cls)

    def setUp(self):
        pass

    def test_stats(self):
        with self.assertTemplateUsed('sales/stats.html'):
            response = self.client.get(reverse('sales:stats:overview'))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['gross'], FruitSales.objects.gross())
