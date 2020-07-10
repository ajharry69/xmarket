import json

from django.contrib.auth import get_user_model
from rest_framework import serializers
from xauth.serializers import RequestSerializer


class ProfileRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'provider',)


class ProfileRequestWithPhotoSerializer(RequestSerializer):
    user = ProfileRequestSerializer()
    photo = serializers.ImageField(
        allow_null=True, allow_empty_file=True, default=None,
        write_only=True,
    )

    def to_representation(self, instance):
        photo, user = instance.get('photo', None), instance.get('user', None)
        user = instance if user is None else user
        user = json.loads(user) if isinstance(user, (str, bytes)) else user
        serializer = ProfileRequestSerializer(data=user, context=self.context)
        user = serializer.data if serializer.is_valid(False) else user
        user['photo'] = photo  # replace photo value in user(dict) with photo file
        return user
