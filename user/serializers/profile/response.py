from rest_framework import serializers

from user.serializers.profile import PublicProfileSerializer


class ProfileResponseSerializer(PublicProfileSerializer):
    photo = serializers.ImageField(
        allow_null=True, allow_empty_file=True, default=None,
        write_only=True,
    )

    class Meta(PublicProfileSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'provider',
                  'photo', 'photo_url', 'is_verified',)
        read_only_fields = ('is_verified', 'photo_url',)
