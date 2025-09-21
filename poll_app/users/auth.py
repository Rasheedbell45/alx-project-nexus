from django.contrib.auth import get_user_model
from rest_framework import serializers, status, generics, permissions
from rest_framework.response import Response

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data.get("email", ""),
            password = validated_data["password"]
        )
        return user

class RegisterAPIView(generics.CreateAPIView):
    """
    POST /api/auth/register/   -> {username, email, password}
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED
        )
