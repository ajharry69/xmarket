from rest_framework.test import APITestCase

from shop.models import Shop, PostalAddress, PhysicalAddress, Coordinates


class TestShop(APITestCase):
    def test_get_products_url(self):
        shop = Shop.objects.create(name='shop1', tax_pin='pin1')
        self.assertEqual(shop.get_products_url(), f'/api/v1/shops/{shop.id}/products/')

    def test_product_to_str(self):
        shop = Shop.objects.create(name='shop1', tax_pin='pin1')

        self.assertEqual(shop.__str__(), f'{shop}')
        self.assertEqual(shop.__str__(), f'shop1')


class TestPostalAddress(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.shop = Shop.objects.create(name='shop1', tax_pin='pin1')

    def test_postal_address_to_str(self):
        address = PostalAddress.objects.create(shop=self.shop, box=1, code=2)
        self.assertEqual(address.__str__(), f'{address}')
        self.assertEqual(address.__str__(), f'1 - 2')


class TestPhysicalAddress(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.shop = Shop.objects.create(name='shop1', tax_pin='pin1')

    def test_default_country_is_kenya(self):
        address = PhysicalAddress.objects.create(shop=self.shop)
        self.assertEqual(address.country.upper(), 'KENYA')

    def test_physical_address_to_str(self):
        address = PhysicalAddress.objects.create(shop=self.shop, major_town='mTown', specific_town='sTown',
                                                 street='street1')
        self.assertEqual(address.__str__(), f'{address}')
        self.assertEqual(address.__str__(), f'sTown, mTown, {address.country}')


class TestCoordinates(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.shop = Shop.objects.create(name='shop1', tax_pin='pin1')

    def test_default_coordinates(self):
        coordinates = Coordinates.objects.create(shop=self.shop)
        self.assertEqual(coordinates.latitude, -1.288457)
        self.assertEqual(coordinates.longitude, 36.823103)
        self.assertEqual(coordinates.altitude, 0.0)

    def test_coordinates_to_str(self):
        coordinates = Coordinates.objects.create(shop=self.shop, latitude=1, longitude=2)
        self.assertEqual(coordinates.__str__(), f'{coordinates}')
        self.assertEqual(coordinates.__str__(), f'1,2')
