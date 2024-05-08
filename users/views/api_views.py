from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class UserDetailApiView(APIView):
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserListApiView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


