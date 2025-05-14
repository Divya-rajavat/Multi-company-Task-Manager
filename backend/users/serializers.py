from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import connection  
from customers.models import Client
from users.models import Theme

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def validate(self, attrs):
        tenant = connection.tenant
        user_count = User.objects.count()

        if user_count >= tenant.user_limit:
            raise serializers.ValidationError("User limit reached for this tenant.")

        return attrs


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['theme_name','primary_color', 'secondary_color', 'background_color', 'font_family']
