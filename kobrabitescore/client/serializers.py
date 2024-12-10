from rest_framework import serializers
from django.contrib.auth import get_user_model
from client.models import Client

User = get_user_model()

# Placeholder for PermissionModelSerializer if needed:
class PermissionModelSerializer(serializers.ModelSerializer):
    pass


class UserBasicSerializer(PermissionModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'validators': []},
            'password': {'validators': []},
        }


class ClientBasicSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'user']
        read_only_fields = ['id']


class ClientSerializer(PermissionModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # If extra fields logic is needed, re-implement it here
        return data


class ClientNestedSerializer(PermissionModelSerializer):
    user = UserBasicSerializer(required=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phone(self, value):
        if value is None or value == '':
            return None
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be digits and 10 characters")
        return value

    def to_internal_value(self, data):
        user_data = data.get('user', None)
        if not user_data:
            raise serializers.ValidationError({"user": "This field is required."})
        if 'email' not in user_data:
            raise serializers.ValidationError({"user": {"email": "This field is required."}})
        if 'password' not in user_data:
            raise serializers.ValidationError({"user": {"password": "This field is required."}})

        ret = super().to_internal_value(data)
        ret['user_data'] = user_data
        return ret

    def create(self, validated_data):
        user_data = validated_data.pop('user_data', None)
        User = get_user_model()
        user = User.objects.create_user(email=user_data['email'], password=user_data['password'])
        validated_data['user'] = user
        client = Client.objects.create(**validated_data)
        return client

    def update(self, instance, validated_data):
        validated_data.pop('user_data', None)  # Don't allow updating user here
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
