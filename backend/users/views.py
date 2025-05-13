from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from users.serializers import CustomUserSerializer

User = get_user_model()

class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
