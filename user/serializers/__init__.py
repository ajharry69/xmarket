from rest_framework import serializers


class RequestSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        return validated_data

    def create(self, validated_data):
        return validated_data
