from rest_framework.test import APITestCase

from products.models import Product, Measurement
from shop.models import Shop


class TestProduct(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.shop = Shop.objects.create(name='shop1', tax_pin='pin1')

    def test_product_to_str(self):
        product = Product.objects.create(shop=self.shop, name='p1', unit_price=1)

        self.assertEqual(product.__str__(), f'{product}')
        self.assertEqual(product.__str__(), f'p1 @ 1/=')


class TestMeasurement(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.shop = Shop.objects.create(name='shop1', tax_pin='pin1')
        self.product = Product.objects.create(shop=self.shop, name='p1', unit_price=1)

    def test_measurement_to_str(self):
        measurement = Measurement.objects.create(product=self.product, quantity=1, unit='g')

        self.assertEqual(measurement.__str__(), f'{measurement}')
        self.assertEqual(measurement.__str__(), f'1g')
