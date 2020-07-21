from rest_framework import serializers

from shop.models import Shop, Coordinates, PhysicalAddress, PostalAddress
from xmarket.utils import pop_data_with_key


class PostalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalAddress
        fields = ('box', 'code',)


class CoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = ('latitude', 'longitude', 'altitude',)


class PhysicalAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalAddress
        fields = ('country', 'major_town', 'specific_town', 'street',)


class ShopSerializer(serializers.HyperlinkedModelSerializer):
    postal_address = PostalAddressSerializer(allow_null=True, default=None, source='postaladdress', )
    address = PhysicalAddressSerializer(allow_null=True, default=None, source='physicaladdress', )
    coordinates = CoordinatesSerializer(allow_null=True, default=None, )

    class Meta:
        model = Shop
        fields = (
            'url', 'id', 'name', 'tax_pin', 'phone', 'email', 'postal_address', 'coordinates', 'address',)

    def update(self, instance, validated_data):
        postal_address = self._postal_address_data(validated_data)
        address = self._physical_address_data(validated_data)
        coordinates = self._coordinates_data(validated_data)
        # all data for nested serializers have already been removed above
        shop = super().update(instance, validated_data)
        poa_instance, pha_instance, coo_instance = None, None, None
        try:
            poa_instance = shop.postaladdress
        finally:
            self._save_postal_address(shop, postal_address, poa_instance)
        try:
            pha_instance = shop.physicaladdress
        finally:
            self._save_physical_address(shop, address, pha_instance)
        try:
            coo_instance = shop.coordinates
        finally:
            self._save_coordinates(shop, coordinates, coo_instance)
        return shop

    def create(self, validated_data):
        postal_address = self._postal_address_data(validated_data)
        address = self._physical_address_data(validated_data)
        coordinates = self._coordinates_data(validated_data)
        # all data for nested serializers have already been removed above
        shop = super().create(validated_data)
        self._save_postal_address(shop, postal_address)
        self._save_physical_address(shop, address)
        self._save_coordinates(shop, coordinates)
        return shop

    def _save_coordinates(self, shop, data, instance=None):
        if data:
            # location coordinates serializer
            lcs = CoordinatesSerializer(instance=instance, data=data, context=self.context, )
            if lcs.is_valid():
                lcs.save(shop=shop)

    def _save_physical_address(self, shop, data, instance=None):
        if data:
            # physical address serializer
            phas = PhysicalAddressSerializer(instance=instance, data=data, context=self.context, )
            if phas.is_valid():
                phas.save(shop=shop)

    def _save_postal_address(self, shop, data, instance=None):
        if data:
            # postal address serializer
            pas = PostalAddressSerializer(instance=instance, data=data, context=self.context, )
            if pas.is_valid():
                pas.save(shop=shop)

    @staticmethod
    def _physical_address_data(validated_data):
        address = pop_data_with_key('address', validated_data)
        # data is sometimes contained in physical address key without underscore because of the source
        # parameter in serializer
        return address if address else pop_data_with_key('physicaladdress', validated_data)

    @staticmethod
    def _postal_address_data(validated_data):
        postal_address = pop_data_with_key('postal_address', validated_data)
        # data is sometimes contained in postal address key without underscore because of the source
        # parameter in serializer
        return postal_address if postal_address else pop_data_with_key('postaladdress', validated_data)

    @staticmethod
    def _coordinates_data(validated_data):
        return pop_data_with_key('coordinates', validated_data)
