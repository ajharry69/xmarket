import json

from rest_framework import serializers
from xauth.serializers import RequestSerializer

from user.serializers.profile.request import ProfileRequestSerializer


class SignUpRequestSerializer(RequestSerializer):
    """
    Data is expected in this format
    {
      "user": {
        "username": "username",
        "email": "username@mail.com",
        "first_name": "John",
        "last_name": "Doe",
        "provider": "EMAIL",
        "is_verified": false
      },
      "password": "securePassword"
    }
    """
    user = ProfileRequestSerializer()
    password = serializers.CharField(
        write_only=True, allow_null=True, allow_blank=True,
        style={'input_type': 'password'},
    )

    def to_representation(self, instance):
        """
        converts instance to dict usable in ProfileResponseSerializer in the following format
        {
          "username": "username",
          "email": "username@mail.com",
          "first_name": "John",
          "last_name": "Doe",
          "provider": "EMAIL",
          "is_verified": false,
          "password": "securePassword"
        }
        """
        request_data = instance.get('user')
        request_data['password'] = instance.get('password')
        return request_data


class SignUpRequestWithPhotoSerializer(RequestSerializer):
    """
    Data is expected in this format
    {
      "user": {
        "user": {
          "username": "username",
          "email": "username@mail.com",
          "first_name": "John",
          "last_name": "Doe",
          "provider": "EMAIL",
          "is_verified": false
        },
        "password": "securePassword"
      },
      "photo": null
    }
    """
    user = SignUpRequestSerializer()
    photo = serializers.ImageField(
        allow_null=True, allow_empty_file=True, default=None,
        write_only=True,
    )

    def to_representation(self, instance):
        """
        converts instance to dict usable in ProfileResponseSerializer in the following format
        {
          "username": "username",
          "email": "username@mail.com",
          "first_name": "John",
          "last_name": "Doe",
          "provider": "EMAIL",
          "is_verified": false,
          "password": "securePassword",
          "photo": null
        }
        """
        photo, user = instance.get('photo', None), instance.get('user', None)
        user = instance if user is None else user
        user = json.loads(user) if isinstance(user, (str, bytes)) else user
        serializer = SignUpRequestSerializer(data=user, context=self.context)
        user = serializer.data if serializer.is_valid(False) else user
        user['photo'] = photo  # replace photo value in user(dict) with photo file
        return user
