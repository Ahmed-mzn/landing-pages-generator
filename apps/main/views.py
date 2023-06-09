from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from django.conf import settings
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from django.http import HttpResponse
from .models import Template, App, Product, Feature, Review, Visit, Domain, TemplateProduct, City, \
    TemplateShare, Lead, MainCity


from .serializers import TemplateSerializer, AppSerializer, AppCreationSerializer, TemplateCreationSerializer, \
    ProductCreationSerializer, FeatureCreationSerializer, ReviewCreationSerializer, VisitSerializer, \
    TemplateProductCreationSerializer, DomainCreationSerializer, \
    BlankTemplateCreationSerializer, LeadSerializer, OrderCreationSerializer, CitySerializer, \
    AppendTemplateChildSerializer, ProductSerializer, TemplateShareSerializer, MainCitySerializer, \
    AppShipSettingSerializer, TemplateMainDetailsSerializer

from apps.ship.models import Order, OrderItem
from apps.ship.serializers import OrderSerializer, OrderItemSerializer


from .resources import OrderResource

from decouple import config
import openai
import requests
import threading


class DomainViewSet(viewsets.ModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainCreationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        validated_data = self.request.data
        if validated_data['type'] == 'normal':
            domain_name = validated_data['name'] + '.sfhat.io'
        else:
            domain_name = validated_data['name']

        serializer.save(user=self.request.user, name=domain_name)

    @action(detail=True, url_path='check_template_name', methods=['post'])
    def check_template_name(self, request, pk):
        template_name = request.data.get('template_name', '')
        domain = get_object_or_404(Domain, pk=pk)
        template_exist = Template.objects.filter(domain=domain, template_name=template_name).exists()
        if template_exist:
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response({'result': False}, status=status.HTTP_200_OK)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(app__user=self.request.user)

    @action(detail=False, url_path='main', methods=['get'])
    def get_main_cities(self, request):
        data = MainCity.objects.all()
        serializer = MainCitySerializer(instance=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='bulk', methods=['post'])
    def bulk_cities(self, request):
        data = request.data
        app = self.request.user.apps.first()
        for item in data:
            City.objects.create(main_city_id=item['id'], app=app)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class TemplateShareViewSet(viewsets.ModelViewSet):
    queryset = TemplateShare.objects.all()
    serializer_class = TemplateShareSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        elif self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            return self.queryset.filter(template__app__user=self.request.user, template_id=template_id)
        return self.queryset.filter(template__app__user=self.request.user)


class VisitAPIView(generics.GenericAPIView):
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            visits = Visit.objects.all().filter(template__app__user=request.user, template_id=template_id)
        else:
            visits = Visit.objects.all().filter(template__app__user=request.user)

        serializer = VisitSerializer(visits, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TemplateCreationSerializer
    queryset = Template.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset.filter(app__user=self.request.user)
        return self.queryset.filter(app__user=self.request.user)

    def retrieve(self, request, pk=None):
        template = get_object_or_404(self.get_queryset().filter(app__user=request.user), pk=pk)
        serializer = self.serializer_class(template)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BlankTemplateCreationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            serializer.instance.make_screenshot()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        template = self.get_object()
        template.soft_delete()
        template.template_name += '(' + template.domain.name.replace('.', '-') + ')'
        template.save()
        if not template.is_child:
            for t in Template.objects.filter(parent=template):
                t.soft_delete()
                t.template_name = t.template_name + '(' + t.domain.name.replace('.', '-') + ')'
                t.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, url_path='short', methods=['get'])
    def short(self, request):
        templates = Template.objects.filter(is_deleted=False, app__user=request.user)
        serializer = TemplateMainDetailsSerializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path='short_details', methods=['get'])
    def short_details(self, request, pk):
        template = get_object_or_404(Template, pk=pk)
        serializer = TemplateMainDetailsSerializer(template, many=False, context={"request":request})
        return Response(serializer.data)

    @action(detail=True, url_path='download_excel', methods=['get'])
    def download_excel(self, request, pk):
        orders = OrderResource(template_id=pk)
        dataset = orders.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="persons.xls"'
        return response

    @action(methods=['GET'], detail=True, url_path="statistics")
    def statistics(self, request, pk):
        template = get_object_or_404(Template, pk=pk)
        templates_child = template.child_templates.all()
        templates = []
        for t in templates_child:
            templates.append({
                "template_name": t.template_name,
                "preview_image": settings.WEBSITE_URL + t.preview_image.url if t.preview_image else '',
                "visits": t.visits.all().count(),
                "orders": t.orders.all().count(),
                "orders_paid": t.orders.all().filter(is_paid=True).count(),
                "customers": Lead.objects.filter(orders__template=t).count(),
                # "income": t.orders.all().aggregate(Sum('amount'))['amount__sum'],
                "shares": t.shares.all().count()
            })
        return Response(data={
            "template": {
                "template_name": template.template_name,
                "preview_image": settings.WEBSITE_URL + template.preview_image.url if template.preview_image else '',
                "url": 'https://' + template.domain.name + '/' + template.template_name,
                "visits": template.visits.all().count(),
                "orders": template.orders.all().count(),
                "orders_paid": template.orders.all().filter(is_paid=True).count(),
                "customers": Lead.objects.filter(orders__template=template).count(),
                # "income": template.orders.all().aggregate(Sum('amount'))['amount__sum'],
                "shares": template.shares.all().count()
            },
            "templates_child": templates
        }, status=status.HTTP_200_OK)

    @action(detail=True, url_path='save_html', methods=['post'])
    def save_html(self, request, pk):
        template = get_object_or_404(Template, pk=pk)
        template.html = request.data.get('html', '')
        template.css = request.data.get('css', '')
        template.js = request.data.get('js', '')
        template.project_data = request.data.get('project_data', '')
        template.save()
        thread = threading.Thread(target=template.make_screenshot(), args=())
        thread.start()
        return Response(data={'mgs': 'success'}, status=status.HTTP_200_OK)

    @action(detail=True, url_path='update_url', methods=['post'])
    def update_url(self, request, pk):
        domain_id = request.data.get('domain', '')
        template_name = request.data.get('template_name', '')

        template = get_object_or_404(Template, pk=pk)
        domain = get_object_or_404(Domain, pk=domain_id)

        if domain and template_name:
            template.domain = domain
            template.template_name = template_name
            for child in template.child_templates.all():
                child.domain = domain
                child.save()
            template.save()
            return Response(data={'mgs': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'errors': 'missing domain or template_name'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="scarp_page", methods=['post'])
    def scarp_page(self, request):
        website_url = request.data.get('website_url', '')
        response = requests.get(website_url)
        text = response.text
        return Response(data={'content': text}, status=status.HTTP_200_OK)


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
    serializer_class = AppShipSettingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # app = get_object_or_404(App, app_id=app_id)
        app = App.objects.filter(user=request.user).first()

        serializer = self.serializer_class(instance=app)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        data = request.data

        # app = get_object_or_404(App, app_id=app_id)
        app = App.objects.filter(user=request.user).first()

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

        # app.delete()

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


class AppendTemplateChildView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = AppendTemplateChildSerializer

    def get(self, request):
        if self.request.GET.get('template_id', ''):
            template_id = self.request.GET.get('template_id', '')
            template = get_object_or_404(Template, pk=template_id)

            template_children = Template.objects.filter(app__user=request.user, is_child=True, parent=template
                                                        , is_deleted=False)
        else:
            template_children = Template.objects.filter(app__user=request.user, is_child=True, is_deleted=False)

        serializer = TemplateSerializer(instance=template_children, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(app=request.user.apps.first())
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArchiveTemplateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = TemplateSerializer

    def get(self, request):
        data = Template.objects.filter(app__user=request.user, is_child=False, is_deleted=True)

        serializer = self.serializer_class(instance=data, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pk = request.data.get('template', '')

        domain = request.data.get('domain', '')

        domain_serializer = DomainCreationSerializer(data=domain)

        if domain_serializer.is_valid():
            domain_obj = domain_serializer.save()

            template = get_object_or_404(Template, pk=pk)

            template.is_deleted = False
            template.domain = domain_obj

            if template.child_templates.all():
                for t in template.child_templates.all():
                    t.is_deleted = False
                    t.domain = domain_obj
                    t.save()

            template.save()

            serializer = self.serializer_class(instance=template, many=False)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=domain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArchiveProductView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = ProductSerializer

    def get(self, request):
        data = Product.objects.filter(app__user=request.user, is_deleted=True)

        serializer = self.serializer_class(instance=data, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        pk = request.data.get('product', '')

        product = get_object_or_404(Product, pk=pk)
        product.is_deleted = False
        product.save()

        serializer = self.serializer_class(instance=product, many=False)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_product_description(request):
    title = request.data.get('title', '')

    openai.api_key = config('CHAT_GPT_API_KEY')
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f'اكتبلي تعريق قصير عن منتج {title} لا يتجاوز ثلاثين حرف ',
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    # headers = {
    #     "Content-Type": "application/json; charset=utf-8",
    #     "Authorization": f"Bearer {config('CHAT_GPT_API_KEY')}"
    # }
    # data = {
    #     "model": "text-davinci-003",
    #     "prompt": "اكتبلي تعريق قصير عن منتج زيت الزيتون لا يتجاوز ثلاثين حرف",
    #     "max_tokens": 1024,
    #     "n": 1,
    #     "stop": "None",
    #     "temperature": 0
    # }
    # url = "https://api.openai.com/v1/completions"
    #
    # response = requests.post(url, headers=headers, json=data)
    #
    # print("Status Code", response.status_code)
    # print("JSON Response ", response.json())

    return Response(
        {
            # "success": response.json()['choices'][0]['text'],
            "result": message,
        },
        status=status.HTTP_201_CREATED
    )


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


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_variant(request):
    data = request.data
    templates = data.get('templates')
    for t in templates:
        if t['is_main_template']:
            template = get_object_or_404(Template, pk=t['id'])
            template.template_redirect_numbers = t['redirect_numbers']
            template.total_redirect_numbers = data.get('total')
            template.next_template = 0
            template.save()
        else:
            template = get_object_or_404(Template, pk=t['id'])
            template.template_redirect_numbers = t['redirect_numbers']
            template.save()
    return Response(data={'success': True}, status=status.HTTP_200_OK)



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_template(request, template_id):
    template = get_object_or_404(Template, pk=template_id)
    serializer = TemplateSerializer(instance=template, many=False)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def check_domain(request):
    # url = f"https://api.cloudflare.com/client/v4/zones/{config('CLOUDFLARE_ZONE_ID')}/dns_records?match=any&name={domain}"
    # headers = {"Authorization": f"Bearer {config('CLOUDFLARE_API_KEY')}"}
    # result = requests.get(url=url, headers=headers).json()
    #
    # if result['result_info']['count'] != 0:
    #     return Response(
    #         {
    #             "result": False,
    #         },
    #         status=status.HTTP_200_OK
    #     )

    domain = request.data.get('domain', '')

    count_domain = Domain.objects.filter(name=domain).count()

    result = True

    if count_domain != 0:
        result = False

    return Response(
        {
            "result": result,
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
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_form(request):
    data = request.data

    serializer = OrderCreationSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
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
def create_share(request):
    data = request.data

    serializer = TemplateShareSerializer(data=data)

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
