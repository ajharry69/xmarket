from django.contrib.auth import get_user_model
from rest_framework import serializers


class PublicProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField(
        default=None, read_only=True, )

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'photo_url', 'is_verified',)

    def get_photo_url(self, user):
        try:
            return self.context.get('request').build_absolute_uri(user.photo.url)
        except (AttributeError, ValueError):
            return None
