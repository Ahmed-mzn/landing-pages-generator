from rest_framework import serializers

from .models import Template, App, Product, FormsRecord
import os


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ('id', 'name', 'path', 'description', 'created_at')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'app', 'title', 'description', 'image', 'price', 'created_at', 'updated_at')


class AppSerializer(serializers.ModelSerializer):
    template = TemplateSerializer(many=False)
    products = ProductSerializer(many=True)

    class Meta:
        model = App
        fields = (
            'id',
            'template',
            'products',
            'app_id',
            'domain',
            'description',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'logo',
            'main_image',
            'created_at',
            'updated_at',
        )


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'description', 'image', 'price')


class AppCreationSerializer(serializers.ModelSerializer):
    products = ProductCreationSerializer(many=True)

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = App
        fields = (
            'template',
            'products',
            'app_id',
            'domain',
            'description',
            'meta_title',
            'meta_description',
            'meta_keywords',
            'logo',
            'main_image',
        )

    def create(self, validated_data):
        products = validated_data.pop('products')
        domain = validated_data.pop('products')

        app = App.objects.create(user=self._user(None), **validated_data)
        os.system(f'ansible-playbook --extra-vars="domain={domain}" --extra-vars="app_id{app.app_id}" '
                  f'/home/khaled/landing_pages/ansible-landing-generator/deploy.yml')

        for product in products:
            Product.objects.create(app=app, **product)
        return app
