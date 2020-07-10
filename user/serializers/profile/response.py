from django.contrib.auth import get_user_model
from rest_framework import serializers


class ProfileResponseSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(
        default=None, read_only=True, )
    photo = serializers.ImageField(
        allow_null=True, allow_empty_file=True, default=None,
        write_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name', 'last_name', 'provider',
                  'photo', 'photo_url', 'is_verified',)
        read_only_fields = ('is_verified', 'photo_url',)

    def get_photo_url(self, user):
        try:
            return self.context.get('request').build_absolute_uri(user.photo.url)
        except (AttributeError, ValueError):
            return None
