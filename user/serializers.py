from django.contrib.auth import get_user_model
from xauth import serializers


class ProfileSerializer(serializers.ProfileSerializer):
    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'email', 'first_name', 'last_name', 'is_verified',)
        read_only_fields = ('is_verified',)
