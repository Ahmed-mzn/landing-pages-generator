from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import UserCreationSerializer, UserDetailSerializer


class UserCreateView(generics.GenericAPIView):
    serializer_class = UserCreationSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)