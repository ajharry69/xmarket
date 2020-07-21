from rest_framework import serializers

from products.models import Product, Measurement
from xmarket.utils import pop_data_with_key


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('quantity', 'unit',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    shop_id = serializers.IntegerField(source='shop.id', read_only=True, )
    measurement = MeasurementSerializer(allow_null=True, default=None, )

    class Meta:
        model = Product
        fields = ('url', 'id', 'shop_id', 'name', 'unit_price', 'measurement',)

    def update(self, instance, validated_data):
        measurement = pop_data_with_key('measurement', validated_data)
        # all data for nested serializers have already been removed above
        product = super().update(instance, validated_data)
        m_instance = None  # measurement instance
        try:
            m_instance = product.measurement
        finally:
            self._save_measurement(product, measurement, m_instance)
        return product

    def create(self, validated_data):
        measurement = pop_data_with_key('measurement', validated_data)
        # all data for nested serializers have already been removed above
        product = super().create(validated_data)
        self._save_measurement(product, measurement)
        return product

    def _save_measurement(self, product, data, instance=None, ):
        if data:
            serializer = MeasurementSerializer(
                instance=instance, data=data, context=self.context, )
            if serializer.is_valid():
                serializer.save(product=product)
                return serializer.data
