from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class UserDetailApiView(APIView):
    @swagger_auto_schema(
        responses={200: CustomUserSerializer()},
        operation_summary="Retrieve a single user by ID",
        operation_description="Retrieve details of a specific user by ID."
    )
    def get(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class UserListApiView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @swagger_auto_schema(
        operation_summary="List all users",
        operation_description="Retrieve a list of all users."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
