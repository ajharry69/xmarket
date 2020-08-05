from rest_framework import serializers

from shopping_list import models
from user.serializers.profile import PublicProfileSerializer


class ProductMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductMeasurement
        fields = ('quantity', 'unit',)


class PurchaseMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PurchaseMeasurement
        fields = ('quantity', 'unit',)


class ShoppingListSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.CharField(source='item_name')
    owner = PublicProfileSerializer(read_only=True, )
    measurement = serializers.DictField(read_only=True, )
    product_measurement = ProductMeasurementSerializer(write_only=True)
    purchase_measurement = PurchaseMeasurementSerializer(write_only=True)

    class Meta:
        model = models.ShoppingList
        fields = (
            'url', 'id', 'item', 'created_on', 'updated_on', 'measurement',
            'product_measurement', 'purchase_measurement', 'owner',)
        read_only_fields = ('id', 'created_on', 'updated_on',)

    def create(self, validated_data):
        product, purchase = self._nested_objects_data(validated_data)
        s_list = super().create(validated_data)
        self._save_product_measurement(s_list, product)
        self._save_purchase_measurement(s_list, purchase)
        return s_list

    def update(self, instance, validated_data):
        product, purchase = self._nested_objects_data(validated_data)
        s_list = super().update(instance, validated_data)
        self._save_product_measurement(s_list, product,
                                       models.ProductMeasurement.objects.filter(shopping_list=s_list).first())
        self._save_purchase_measurement(s_list, purchase,
                                        models.PurchaseMeasurement.objects.filter(shopping_list=s_list).first())
        return s_list

    @staticmethod
    def _nested_objects_data(validated_data):
        product = validated_data.pop(
            'product_measurement') if 'product_measurement' in validated_data else None
        purchase = validated_data.pop(
            'purchase_measurement') if 'purchase_measurement' in validated_data else None
        return product, purchase

    @staticmethod
    def _save_purchase_measurement(s_list, data, instance=None):
        if data:
            sr = PurchaseMeasurementSerializer(data=data)
            if sr.is_valid():
                return sr.save(shopping_list=s_list)

    @staticmethod
    def _save_product_measurement(s_list, data, instance=None):
        if data:
            sr = ProductMeasurementSerializer(data=data)
            if sr.is_valid():
                return sr.save(shopping_list=s_list)
