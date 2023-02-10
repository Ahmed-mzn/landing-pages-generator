from rest_framework import serializers

from .models import User
from apps.main.models import App


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=85)
    full_name = serializers.CharField(max_length=25)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
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

        App.objects.create(user=user)

        return user


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone_number', 'is_active')
