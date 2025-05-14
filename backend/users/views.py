from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from users.serializers import CustomUserSerializer, ThemeSerializer
from django.http import Http404
from users.models import Theme
from django.db import connection

User = get_user_model()

class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)


class ThemeSettingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        connection.set_schema(request.tenant.schema_name)

        themes = Theme.objects.all()
        if not themes.exists():
            return Response({"error": "No themes found for this tenant."}, status=404)

        serializer = ThemeSerializer(themes, many=True)  
        return Response(serializer.data)
