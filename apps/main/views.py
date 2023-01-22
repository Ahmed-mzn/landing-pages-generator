from django.shortcuts import render, get_object_or_404

from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Template, App, Product, FormsRecord, Feature, Review, Visit, Domain, TemplateProduct

from .serializers import TemplateSerializer, AppSerializer, AppCreationSerializer, TemplateCreationSerializer, \
    ProductCreationSerializer, FeatureCreationSerializer, ReviewCreationSerializer, VisitSerializer, \
    FormsRecordSerializer, FormsRecordCreationSerializer, TemplateProductCreationSerializer, DomainCreationSerializer, \
    BlankTemplateCreationSerializer

from decouple import config
import requests


class VisitAPIView(generics.GenericAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        visits = Visit.objects.all().filter(template__app__user=request.user)

        serializer = VisitSerializer(visits, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FormAPIView(generics.GenericAPIView):
    serializer_class = FormsRecordSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            forms = FormsRecord.objects.all().filter(template__app__user=request.user, template_id=template_id)
        else:
            forms = FormsRecord.objects.all().filter(template__app__user=request.user)

        serializer = FormsRecordSerializer(forms, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateCreationSerializer
    queryset = Template.objects.all().filter(is_deleted=False)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(app__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        template = self.get_object()
        template.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductCreationSerializer
    queryset = Product.objects.all().filter(is_deleted=False)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            return self.queryset.filter(app__user=self.request.user, product_templates__template_id=template_id)
        return self.queryset.filter(app__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        product.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class FeatureViewSet(viewsets.ModelViewSet):
    serializer_class = FeatureCreationSerializer
    queryset = Feature.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            return self.queryset.filter(template__app__user=self.request.user, template_id=template_id)
        return self.queryset.filter(template__app__user=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewCreationSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            return self.queryset.filter(template__app__user=self.request.user, template_id=template_id)
        return self.queryset.filter(template__app__user=self.request.user)


class AppRetrieveDeleteUpdateView(generics.GenericAPIView):
    serializer_class = AppCreationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, app_id):

        app = get_object_or_404(App, app_id=app_id)

        serializer = self.serializer_class(instance=app)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, app_id):
        data = request.data

        app = get_object_or_404(App, app_id=app_id)

        serializer = self.serializer_class(data=data, instance=app)

        if serializer.is_valid():
            serializer.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, app_id):
        app = get_object_or_404(App, app_id=app_id)

        # if app.domain.type == 'normal':
        #     print('delete normal domain')
        #     url = f"https://api.cloudflare.com/client/v4/zones/{config('CLOUDFLARE_ZONE_ID')}/dns_records/{app.domain.record_id}"
        #     headers = {"Authorization": f"Bearer {config('CLOUDFLARE_API_KEY')}"}
        #     result = requests.delete(url=url, headers=headers).json()

        app.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AppByIdView(generics.GenericAPIView):
    serializer_class = AppSerializer
    permission_classes = []
    authentication_classes = []

    def get(self, request, app_id):
        # try:
        app = App.objects.get(app_id=app_id)
        templates = app.templates.all().order_by("id")

        if app.next_template == 0:
            app.next_template = templates[0].id
            app.save()
        else:
            # print("next temp: ", app.next_template)

            template_ids = [t.id for t in templates]
            # print("temp ids: ", template_ids)

            current_temp_id_index = template_ids.index(app.next_template)
            # print("current index: ", current_temp_id_index)

            if current_temp_id_index == (len(template_ids) - 1):
                app.next_template = template_ids[0]
                app.save()
            else:
                app.next_template = template_ids[current_temp_id_index + 1]
                app.save()

        serializer = self.serializer_class(instance=app, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # except:
        #     return Response(data={'msg': 'app not found'}, status=status.HTTP_400_BAD_REQUEST)


class AppCreationListView(generics.GenericAPIView):
    serializer_class = AppCreationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = AppCreationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssignProductToTemplateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TemplateProductCreationSerializer

    def post(self, request, template_id, product_id):
        try:
            template_product = TemplateProduct.objects.get(template_id=template_id, product_id=product_id)
            return Response(data={"message": "product already exist in the template"},
                            status=status.HTTP_400_BAD_REQUEST)
        except:

            data = {
                'template': template_id,
                'product': product_id,
            }
            serializer = self.serializer_class(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, template_id, product_id):
        template_product = get_object_or_404(TemplateProduct, template_id=template_id, product_id=product_id)
        template_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateDomainView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DomainCreationSerializer

    def put(self, request, pk):

        domain = get_object_or_404(Domain, pk=pk)

        serializer = self.serializer_class(data=request.data, instance=domain)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_blank_template(request):
    serializer = BlankTemplateCreationSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_app(request):
    app = request.user.apps.first()
    serializer = AppSerializer(instance=app, many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    serializer = TemplateSerializer(instance=template, many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_domain(request, domain):
    url = f"https://api.cloudflare.com/client/v4/zones/{config('CLOUDFLARE_ZONE_ID')}/dns_records?match=any&name={domain}"
    headers = {"Authorization": f"Bearer {config('CLOUDFLARE_API_KEY')}"}
    result = requests.get(url=url, headers=headers).json()

    if result['result_info']['count'] != 0:
        return Response(
            {
                "result": False,
            },
            status=status.HTTP_200_OK
        )

    return Response(
        {
            "result": True,
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_visit(request):
    data = request.data
    data['json_object'] = str(request.META)
    serializer = VisitSerializer(data=data)

    if serializer.is_valid():
        serializer.save(ip_address=request.META['REMOTE_ADDR'])
        return Response(
            {
                "success": True,
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_form(request):
    data = request.data
    serializer = FormsRecordCreationSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
            },
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_template_one(request, app_id):
    template = get_object_or_404(Template, app__app_id=app_id, template_code="template_one")
    serializer = TemplateSerializer(template, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_template_two(request, app_id):
    template = get_object_or_404(Template, app__app_id=app_id, template_code="template_two")
    serializer = TemplateSerializer(template, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)
