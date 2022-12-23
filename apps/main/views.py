from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Template, App, Product, FormsRecord

from .serializers import TemplateSerializer, AppSerializer, AppCreationSerializer


class TemplateLisView(generics.GenericAPIView):
    serializer_class = TemplateSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        templates = Template.objects.all()

        serializer = self.serializer_class(instance=templates, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AppLisView(generics.GenericAPIView):
    serializer_class = AppSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        apps = App.objects.all()

        serializer = self.serializer_class(instance=apps, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AppByIdLisView(generics.GenericAPIView):
    serializer_class = AppSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request, app_id):
        try:
            app = App.objects.get(app_id=app_id)

            serializer = self.serializer_class(instance=app, many=False)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={'msg': 'app not found'}, status=status.HTTP_400_BAD_REQUEST)


class AppCreationListView(generics.GenericAPIView):
    serializer_class = AppCreationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = AppCreationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
