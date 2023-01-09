from rest_framework import serializers
import requests
from decouple import config
from .models import Template, App, Product, FormsRecord, Feature, Review, Domain, Visit
from .threads import CreateDeployAppThread


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ('id', 'template', 'city', 'region', 'country', 'location', 'ip_address', 'duration', 'json_object',
                  'created_at', 'updated_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'template', 'title', 'description', 'image', 'price', 'price_after_discount', 'created_at',
                  'updated_at')


class FormsRecordSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = FormsRecord
        fields = ('id', 'template', 'product', 'quantity', 'name', 'phone_number', 'city', 'address', 'created_at',
                  'updated_at')


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
    products = ProductSerializer(many=True)
    customer_website = serializers.SerializerMethodField()

    def get_customer_website(self, obj):
        return obj.app.customer_website

    # def get_products(self, obj):
    #     print(obj)
    #     data = Product.objects.all().filter(product_templates__template_id=obj.id)
    #
    #     products = ProductSerializer(data, many=True)
    #     return products.data

    class Meta:
        model = Template
        fields = ('id', 'template_code', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'logo',
                  'main_image', 'medals_image', 'second_image', 'review_text', 'primary_color', 'secondary_color',
                  'products', 'features', 'reviews', 'customer_website', 'created_at', 'updated_at')


class AppSerializer(serializers.ModelSerializer):
    templates = TemplateSerializer(many=True)
    domain = DomainSerializer(many=False)

    class Meta:
        model = App
        fields = (
            'id',
            'app_id',
            'customer_website',
            'next_template',
            'domain',
            'templates',
            'created_at',
            'updated_at',
        )


# Creation Serializers

class FormsRecordCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsRecord
        fields = ('id', 'template', 'product', 'quantity', 'name', 'phone_number', 'city', 'address', 'created_at',
                  'updated_at')


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'template', 'title', 'description', 'image', 'price', 'price_after_discount')


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
        fields = ('id', 'app', 'template_code', 'description', 'meta_title', 'meta_description', 'meta_keywords', 'logo',
                  'main_image', 'medals_image', 'second_image', 'review_text', 'primary_color',
                  'secondary_color')


class AppCreationSerializer(serializers.ModelSerializer):
    domain = DomainSerializer(many=False)

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
            'domain',
            'customer_website',
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
        domain_data = validated_data.pop('domain')

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
        domain = Domain.objects.create(app=app, record_id='None', **domain_data)

        # create two templates

        Template.objects.create(app=app, template_code="template_one")
        Template.objects.create(app=app, template_code="template_two")

        #os.system(f'/home/khaled/landing_pages/landing-pages-generator/venv/bin/ansible-playbook --extra-vars="domain={domain}" --extra-vars="app_id={app.app_id}" /home/khaled/landing_pages/ansible-landing-generator/deploy.yml')

        CreateDeployAppThread(domain.name, app.app_id).start()

        return app
