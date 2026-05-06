from rest_framework import generics

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):

    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
