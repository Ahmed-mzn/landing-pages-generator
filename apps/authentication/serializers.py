from rest_framework import serializers

from .models import User
from apps.main.models import App, Domain, Template, City

from apps.main.openship import create_user
import uuid


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=85)
    full_name = serializers.CharField(max_length=25)
    business_name = serializers.CharField(max_length=25, default='')
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'business_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise serializers.ValidationError(detail="User with email exists")

        return super().validate(attrs)

    def create(self, validated_data):

        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            full_name=validated_data['full_name'],
            password_plain_text=validated_data['password']
        )

        user.set_password(validated_data['password'])
        user.save()

        create_user(validated_data['full_name'], validated_data['email'], validated_data['password'],
                    validated_data['business_name'])

        app = App.objects.create(user=user, business_name=validated_data['business_name'])

        domain_name = str(uuid.uuid4()) + '.sfhat.io'
        domain = Domain.objects.create(type='normal', name=domain_name)

        template = Template.objects.create(domain=domain, template_name='main', app=app, template_code='template_one',
                                           template_redirect_numbers=10, total_redirect_numbers=10)

        City.objects.create(app=app, name='الرياض')
        City.objects.create(app=app, name='مكة المكرمة')
        City.objects.create(app=app, name='المدينة المنورة')
        City.objects.create(app=app, name='الدمام')
        City.objects.create(app=app, name='تبوك')
        City.objects.create(app=app, name='جدة')

        return user


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone_number', 'is_active')


class UserResetPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, write_only=True)
    new_password = serializers.CharField(min_length=6, write_only=True)
    new_password2 = serializers.CharField(min_length=6, write_only=True)

    def _user(self, obj):
        request = self.context.get('request', None)
        if request:
            return request.user

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')
        extra_kwargs = {
            'old_password': {'write_only': True},
            'new_password': {'write_only': True},
            'new_password2': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(detail="Password does not match")

        if self._user(None).password_plain_text != attrs['old_password']:
            raise serializers.ValidationError(detail="Wrong password")

        return attrs

    def create(self, validated_data):
        user = self._user(None)
        user.set_password(validated_data['new_password'])
        user.password_plain_text = validated_data['new_password']

        user.save()

        return user
