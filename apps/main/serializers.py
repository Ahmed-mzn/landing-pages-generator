from rest_framework import serializers
import requests, random
from decouple import config
from django.conf import settings
from .models import Template, App, Product, FormsRecord, Feature, Review, Domain, Visit, TemplateProduct, Lead, City, \
    TemplateShare
from .threads import CreateDeployAppThread


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'app', 'name', 'created_at', 'updated_at')


class TemplateShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateShare
        fields = ('id', 'template', 'phone_number', 'city', 'created_at', 'updated_at')


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
        return settings.WEBSITE_URL + 'static/assets/img/hero.png'

    def get_medals_image_url(self, obj):
        if obj.medals_image:
            return settings.WEBSITE_URL + obj.medals_image.url
        return settings.WEBSITE_URL + 'static/assets/img/Rectangle 1249.png'

    def get_second_image_url(self, obj):
        if obj.second_image:
            return settings.WEBSITE_URL + obj.second_image.url
        return settings.WEBSITE_URL + 'static/assets/img/olivia.png'

    def get_products(self, obj):
        data = Product.objects.all().filter(product_templates__template_id=obj.id, is_deleted=False)

        products = ProductSerializer(data, many=True)
        return products.data

    class Meta:
        model = Template
        fields = ('id', 'app', 'template_code', 'template_name', 'domain', 'description', 'meta_title',
                  'meta_description', 'cities', 'meta_keywords', 'logo', 'main_image', 'medals_image', 'second_image',
                  'review_text', 'primary_color', 'secondary_color', 'products', 'features', 'reviews',
                  'customer_website', 'feature_text', 'total_redirect_numbers', 'template_redirect_numbers',
                  'template_redirect_percentage', 'is_child', 'is_deleted', 'created_at', 'updated_at')


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
    parent_template = serializers.IntegerField(allow_null=True, default=0)
    is_copy = serializers.BooleanField(default=True)

    class Meta:
        model = Template
        fields = ('template', 'template_name', 'template_code', 'parent_template', 'is_copy')

    def validate_template(self, value):
        try:
            Template.objects.get(pk=value)
        except:
            raise serializers.ValidationError(detail="Template not found")

        return value

    def validate_parent_template(self, value):
        try:
            Template.objects.get(pk=value)
        except:
            raise serializers.ValidationError(detail="Template not found")

        return value

    def create(self, validated_data):
        template_id = validated_data.pop('template')
        parent_template_id = validated_data.pop('parent_template')
        is_copy = validated_data.pop('is_copy')

        parent_template = Template.objects.get(pk=parent_template_id)
        template = Template.objects.get(pk=template_id)
        new_template = Template.objects.get(pk=template_id)

        if is_copy:
            new_template.parent_id = parent_template.pk
            new_template.pk = None
            new_template.is_child = True
            new_template.template_redirect_numbers = 0
            new_template.next_template = 0
            new_template.next_template_redirect_numbers = 0
            new_template.total_redirect_numbers = 0
            new_template.template_name = template.template_name \
                                         + '-copy(' + str(template.child_templates.count()+1) + ')'
            new_template.save()

            # make copy of features
            for f in template.features.all():
                Feature.objects.create(template=new_template, title=f.title, description=f.description)

            # make copy of reviews
            for r in template.reviews.all():
                Review.objects.create(template=new_template, username=r.username, comment=r.comment, rating=r.rating)

            # make copy of products
            for p in template.template_products.all():
                TemplateProduct.objects.create(template=new_template, product=p.product)

        else:
            new_template = Template.objects.create(domain=template.domain, parent=parent_template, is_child=True,
                                                   **validated_data)

        return new_template


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
        print(validated_data['product'])
        try:
            lead = Lead.objects.all().get(phone_number=validated_data.get('phone_number'))
            validated_data.pop('name')
            validated_data.pop('phone_number')
            validated_data.pop('city')
            validated_data.pop('address')
        except:
            lead = Lead.objects.create(name=validated_data.pop('name'), phone_number=validated_data.pop('phone_number'),
                                       city=validated_data.pop('city'), address=validated_data.pop('address'))
        product = validated_data['product']
        if product.price_after_discount:
            amount = validated_data['quantity'] * product.price_after_discount
        else:
            amount = validated_data['quantity'] * product.price
        form = FormsRecord.objects.create(lead=lead, amount=amount, **validated_data)

        return form


class DomainCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'name', 'type')

    def create(self, validated_data):
        if validated_data['type'] == 'normal':
            domain_name = validated_data['name'] + '.sfhat.io'

        domain = Domain.objects.create(name=domain_name, type=validated_data['type'])

        return domain


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

        template = Template.objects.create(domain=domain_obj, next_template_redirect_numbers=0, next_template=0,
                                           template_redirect_numbers=0, **validated_data)

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
    domain = DomainSerializer(many=False)

    class Meta:
        model = Template
        fields = ('id', 'app', 'domain', 'template_code', 'template_name', 'description', 'meta_title',
                  'meta_description', 'meta_keywords', 'main_image', 'medals_image', 'second_image', 'feature_text',
                  'total_redirect_numbers', 'template_redirect_numbers', 'template_redirect_percentage',
                  'review_text', 'customer_website', 'primary_color', 'secondary_color', 'is_child')
        read_only_fields = (
            'domain',
            'total_redirect_numbers', 'template_redirect_numbers', 'template_redirect_percentage',
        )


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
