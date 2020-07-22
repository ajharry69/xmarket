from rest_framework import serializers

from receipt import models


class ReceiptSerializer(serializers.HyperlinkedModelSerializer):
    receipt = serializers.ImageField(write_only=True, )
    receipt_url = serializers.SerializerMethodField(read_only=True, method_name='get_receipt', )

    class Meta:
        model = models.Receipt
        fields = ('receipt', 'receipt_url',)

    def to_representation(self, instance):
        return self.get_receipt(instance)

    def get_receipt(self, receipt):
        url = None
        try:
            url = self.context.get('request').build_absolute_uri(receipt.receipt.url)
        finally:
            return url
