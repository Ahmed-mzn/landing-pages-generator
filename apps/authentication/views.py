from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UserCreationSerializer


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
