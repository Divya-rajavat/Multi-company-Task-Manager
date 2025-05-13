from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['schema_name', 'name']
