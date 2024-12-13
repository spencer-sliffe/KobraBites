from rest_framework import serializers
from django.contrib.auth import get_user_model
from client.models import Client
from user.serializers import UserBasicSerializer

User = get_user_model()


class ClientSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'birthdate', 'phone', 'pronouns', 'gender',
                  'user', 'email_opt_in', 'phone_opt_in']
        read_only_fields = fields


class ClientNestedSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(required=True)
    birthdate = serializers.DateField(required=False, allow_null=True)

    class Meta:
        model = Client
        fields = [
            'id', 'first_name', 'last_name', 'birthdate', 'phone',
            'pronouns', 'gender', 'user', 'email_opt_in', 'phone_opt_in'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_internal_value(self, data):
        user_data = data.get('user', None)
        if not user_data:
            raise serializers.ValidationError({"user": "This field is required."})
        if 'email' not in user_data:
            raise serializers.ValidationError({"user": {"email": "This field is required."}})
        if 'password' not in data.get('user', {}):
            raise serializers.ValidationError({"user": {"password": "This field is required."}})

        return super().to_internal_value(data)

    def create(self, validated_data):
        user_data = self.initial_data['user']
        email = user_data['email']
        password = user_data['password']
        username = user_data['username']

        user = User.objects.create_user(
            email=email,
            password=password,
            username=username
        )
        validated_data['user'] = user
        client = Client.objects.create(**validated_data)
        return client
