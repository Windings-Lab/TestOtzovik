from rest_framework import serializers

from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'picture', 'profile_link']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data['access_token'] = instance.get_access_token()
    #     data['refresh_token'] = instance.get_refresh_token()
    #     return data
