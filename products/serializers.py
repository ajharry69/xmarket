from rest_framework import serializers
from rest_framework.reverse import reverse

from products.models import Product, Measurement
from xmarket.utils import pop_data_with_key


class ProductHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    queryset = Product.objects.all()
    view_name = 'product-detail'

    def get_queryset(self):
        return super().get_queryset()

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
            'shop_id': view_kwargs['shop_id'],
            'pk': view_kwargs['pk'],
        }
        return self.get_queryset().get(**lookup_kwargs)

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            'shop_id': obj.shop.id,
            'pk': obj.pk,
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)


class ProductHyperlinkedIdentityField(ProductHyperlinkedRelatedField):
    queryset = None

    def __init__(self, view_name=None, **kwargs):
        assert view_name is not None, 'The `view_name` argument is required.'
        kwargs['read_only'] = True
        kwargs['source'] = '*'
        super().__init__(view_name, **kwargs)

    def use_pk_only_optimization(self):
        # We have the complete object instance already. We don't need
        # to run the 'only get the pk for this relationship' code.
        return False


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('quantity', 'unit',)


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # serializer_url_field = ProductHyperlinkedIdentityField
    url = ProductHyperlinkedIdentityField(view_name='product-detail', read_only=True, )
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
