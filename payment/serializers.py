from rest_framework import serializers


class StripeClientSecretSerializer(serializers.Serializer):
    amount = serializers.FloatField()

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
