from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework import serializers

from user.tasks import user_set_reset_token

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',   
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login'
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'is_superuser', 'last_login']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['password'] = ''
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        updated = {'updated_at'}
        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                # Don't actually allow them to change email
                if attr in {'email', 'password'}:
                    raise serializers.ValidationError(f"Cannot change {attr}")
                setattr(instance, attr, value)
                updated.add(attr)
        instance.save(update_fields=updated)
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid email or password')
        data['user'] = user
        return data


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        users = User.objects.filter(email__iexact=email).all()
        if len(users) == 1:
            return users[0].email
        return email

    def create(self, validated_data):
        users = User.objects.filter(email=validated_data['email']).all()
        if len(users) != 1:
            raise serializers.ValidationError('Invalid email')
        user = users[0]
        user_set_reset_token(user)
        return user


class ValidateTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user = User.get_user_by_uidb64(data['uid'])
        except Exception:
            raise serializers.ValidationError({'non_field_errors': ['Invalid password reset link']})
        if user.reset_token != data['token']:
            raise serializers.ValidationError({'non_field_errors': ['This token is no longer valid']})
        if user.reset_token_expires < timezone.now():
            raise serializers.ValidationError({'non_field_errors': ['This token has expired, please request another']})
        return data


class SetNewPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        password1 = []
        password2 = []
        errors = {}
        if len(data['password1']) < 8:
            password1.append('Password must be at least 8 characters')
        if not any(char.isdigit() for char in data['password1']):
            password1.append('Password must contain at least one digit')
        if not any(char.isupper() for char in data['password1']):
            password1.append('Password must contain at least one uppercase letter')
        if data['password1'] != data['password2']:
            password2.append('Passwords do not match')
        if password1:
            errors['password1'] = password1
        if password2:
            errors['password2'] = password2
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def update(self, instance, validated_data):
        if instance.reset_token != validated_data['token']:
            raise serializers.ValidationError({'non_field_errors': ['This token is no longer valid']})
        if instance.reset_token_expires < timezone.now():
            raise serializers.ValidationError({'non_field_errors': ['This token has expired, please request another']})
        instance.set_password(validated_data['password1'])
        instance.reset_token = None
        instance.reset_token_expires = None
        instance.save(update_fields=['password', 'reset_token', 'reset_token_expires'])
        return instance
