from rest_framework import serializers
import requests
from decouple import config
from django.conf import settings
from .models import Template, App, Product, FormsRecord, Feature, Review, Domain, Visit, TemplateProduct, Lead, City
from .threads import CreateDeployAppThread


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'app', 'name', 'created_at', 'updated_at')


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id', 'template', 'city', 'region', 'country', 'location', 'ip_address', 'duration', 'json_object',
                  'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, obj):
        if obj.image:
            return settings.WEBSITE_URL + obj.image.url
        return ''

    class Meta:
        model = Product
        fields = ('id', 'app', 'title', 'description', 'image', 'price', 'price_after_discount', 'created_at',
                  'updated_at')


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ('id', 'name', 'phone_number', 'city', 'address', 'created_at', 'updated_at')


class FormsRecordSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(many=False, read_only=True)
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = FormsRecord
        fields = ('id', 'lead', 'template', 'product', 'quantity', 'created_at', 'updated_at')


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'name', 'type', 'record_id', 'created_at', 'updated_at')


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'title', 'description', 'created_at', 'updated_at')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'username', 'comment', 'rating', 'created_at', 'updated_at')


class TemplateSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    domain = DomainSerializer(many=False)
    products = serializers.SerializerMethodField(method_name="get_products")
    cities = serializers.SerializerMethodField(method_name="get_cities")
    # template_children = serializers.SerializerMethodField(method_name="get_template_children")
    logo = serializers.SerializerMethodField('get_logo_url')
    main_image = serializers.SerializerMethodField('get_main_image_url')
    medals_image = serializers.SerializerMethodField('get_medals_image_url')
    second_image = serializers.SerializerMethodField('get_second_image_url')

    # def get_template_children(self, obj):
    #     data = Template.objects.all().filter(domain=obj.domain, is_child=True)
    #     children = TemplateCreationSerializer(data, many=True)
    #
    #     return children.data

    def get_cities(self, obj):
        data = City.objects.all().filter(app=obj.app)

        cities = CitySerializer(data, many=True)
        return cities.data

    def get_logo_url(self, obj):
        if obj.logo:
            return settings.WEBSITE_URL + obj.logo.url
        return  ''

    def get_main_image_url(self, obj):
        if obj.main_image :
            return settings.WEBSITE_URL + obj.main_image.url
        return ''

    def get_medals_image_url(self, obj):
        if obj.medals_image:
            return settings.WEBSITE_URL + obj.medals_image.url
        return ''

    def get_second_image_url(self, obj):
        if obj.second_image:
            return settings.WEBSITE_URL + obj.second_image.url
        return ''

    def get_products(self, obj):
        data = Product.objects.all().filter(product_templates__template_id=obj.id)

        products = ProductSerializer(data, many=True)
        return products.data

    class Meta:
        model = Template
        fields = ('id', 'template_code', 'template_name', 'domain', 'description', 'meta_title', 'meta_description',
                  'cities', 'meta_keywords', 'logo', 'main_image', 'medals_image', 'second_image', 'review_text',
                  'primary_color', 'secondary_color', 'products', 'features', 'reviews', 'customer_website',
                  'is_child', 'is_deleted', 'created_at', 'updated_at')


class AppSerializer(serializers.ModelSerializer):
    templates = serializers.SerializerMethodField('get_templates')

    def get_templates(self, obj):
        data = Template.objects.all().filter(app_id=obj.id, is_deleted=False, is_child=False)

        templates = TemplateSerializer(data, many=True)
        return templates.data

    class Meta:
        model = App
        fields = (
            'id',
            'app_id',
            'next_template',
            'templates',
            'created_at',
            'updated_at',
        )


# Creation Serializers

class AppendTemplateChildSerializer(serializers.ModelSerializer):
    template = serializers.IntegerField(allow_null=True)
    is_copy = serializers.BooleanField(default=True)

    class Meta:
        model = Template
        fields = ('template', 'template_name', 'template_code', 'is_copy')

    def validate_template(self, value):
        try:
            Template.objects.get(pk=value)
        except:
            raise serializers.ValidationError(detail="Template not found")

        return value

    def create(self, validated_data):
        template_id = validated_data.pop('template')
        is_copy = validated_data.pop('is_copy')

        template = Template.objects.get(pk=template_id)

        if is_copy:
            template.pk = None
            template.is_child = True
            template.template_name = validated_data['template_name']
            template.save()
        else:
            new_template = Template.objects.create(domain=template.domain, is_child=True, **validated_data)
            template = new_template

        return template


class FormsRecordCreationSerializer(serializers.ModelSerializer):
    lead = LeadSerializer(many=False, read_only=True)
    quantity = serializers.IntegerField()
    name = serializers.CharField()
    phone_number = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = FormsRecord
        fields = ('id', 'lead', 'template', 'product', 'quantity', 'name', 'phone_number', 'city', 'address',
                  'created_at', 'updated_at')

    def create(self, validated_data):
        try:
            lead = Lead.objects.all().get(phone_number=validated_data.get('phone_number'))
            validated_data.pop('name')
            validated_data.pop('phone_number')
            validated_data.pop('city')
            validated_data.pop('address')
        except:
            lead = Lead.objects.create(name=validated_data.pop('name'), phone_number=validated_data.pop('phone_number'),
                                       city=validated_data.pop('city'), address=validated_data.pop('address'))

        form = FormsRecord.objects.create(lead=lead, **validated_data)

        return form


class DomainCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'name', 'type')


class BlankTemplateCreationSerializer(serializers.ModelSerializer):
    domain = DomainCreationSerializer(many=False)

    class Meta:
        model = Template
        fields = ('id', 'app', 'domain', 'template_code', 'template_name')

    def validate_domain(self, value):
        domain_name = value['name']
        if value['type'] == 'normal':
            domain_name = value['name']+'.sfhat.io'

        domain_exist = Domain.objects.filter(name=domain_name).exists()

        if domain_exist:
            raise serializers.ValidationError(detail="Domain already exists")

        return value

    def create(self, validated_data):

        domain = validated_data.pop('domain')
        domain_name = domain['name']

        if domain['type'] == 'normal':
            domain_name = domain['name']+'.sfhat.io'

        domain_obj = Domain.objects.create(name=domain_name, type=domain['type'])

        template = Template.objects.create(domain=domain_obj, **validated_data)

        return template


class TemplateProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateProduct
        fields = ('id', 'template', 'product')


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'app', 'title', 'description', 'image', 'price', 'price_after_discount')


class FeatureCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'template', 'title', 'description')


class ReviewCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'template', 'username', 'comment', 'rating')


class TemplateCreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = ('id', 'app', 'template_code', 'template_name', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'logo',
                  'main_image', 'medals_image', 'second_image', 'review_text', 'customer_website', 'primary_color',
                  'secondary_color')


class AppCreationSerializer(serializers.ModelSerializer):

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = App
        read_only_fields = (
            'app_id',
            'next_template',
            'created_at',
            'updated_at',
        )
        fields = (
            'id',
            'app_id',
            'next_template',
            'created_at',
            'updated_at',
        )

    # def validate(self, attrs):
    #     if attrs['domain']['type'] == 'normal':
    #         domain = attrs['domain']['name']
    #         url = f"https://api.cloudflare.com/client/v4/zones/{config('CLOUDFLARE_ZONE_ID')}/dns_records?match=any&name={domain}"
    #         headers = {"Authorization": f"Bearer {config('CLOUDFLARE_API_KEY')}"}
    #         result = requests.get(url=url, headers=headers).json()
    #
    #         if result['result_info']['count'] != 0:
    #             raise serializers.ValidationError(detail="Domain already exist")
    #
    #     return super().validate(attrs)

    def validate(self, attrs):
        if self._user(None).apps.all().count() != 0:
            raise serializers.ValidationError(detail="Already exist app")
        return super().validate(attrs)

    def create(self, validated_data):

        # url = f"https://api.cloudflare.com/client/v4/zones/{config('CLOUDFLARE_ZONE_ID')}/dns_records"
        # headers = {"Authorization": f"Bearer {config('CLOUDFLARE_API_KEY')}"}
        # data = {
        #     "type": "A",
        #     "name": domain_data['name'],
        #     "content": config('SERVER_IP'),
        #     "ttl": 1
        # }
        #
        # result = requests.post(url=url, json=data, headers=headers).json()
        #
        # if not result['success']:
        #     raise serializers.ValidationError(detail="Error, on creating domain")

        app = App.objects.create(user=self._user(None), **validated_data)

        # domain = Domain.objects.create(app=app, record_id=result['result']['id'], **domain_data)

        # create two templates

        Template.objects.create(app=app, template_code="template_one")

        #os.system(f'/home/khaled/landing_pages/landing-pages-generator/venv/bin/ansible-playbook --extra-vars="domain={domain}" --extra-vars="app_id={app.app_id}" /home/khaled/landing_pages/ansible-landing-generator/deploy.yml')

        CreateDeployAppThread('domain.name', app.app_id).start()

        return app
