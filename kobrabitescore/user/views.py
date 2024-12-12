import logging
from django.contrib.auth import logout, login
from django.middleware.csrf import get_token
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from user.serializers import UserSerializer, User, LoginSerializer
from client.serializers import ClientNestedSerializer
from client.access import PUTLESS_METHODS

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = PUTLESS_METHODS
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        # Allow any user to register
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        # Use ClientNestedSerializer for creation (registration),
        # which creates both User and Client.
        if self.action == 'create':
            return ClientNestedSerializer
        return UserSerializer


@extend_schema(tags=["register"])
class RegisterViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="register",
        request=ClientNestedSerializer,
        responses={201: UserSerializer, 400: {}},
        examples=[OpenApiExample(
            "Register Example",
            value={
                "user": {
                    "email": "test@example.com",
                    "username": "testuser",
                    "password": "password123"
                },
                "first_name": "John",
                "last_name": "Doe",
                "phone": "1234567890",
                "pronouns": "he/him",
                "gender": "male",
                "email_opt_in": True,
                "phone_opt_in": False
            }
        )],
    )
    def create(self, request):
        serializer = ClientNestedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        user = client.user
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["login"])
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="login",
        request=LoginSerializer,
        responses={201: UserSerializer, 400: {}},
    )
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)  # Sets session cookie
        return Response(UserSerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="get_current_user",
        responses={200: UserSerializer}
    )
    def list(self, request):
        get_token(request)
        if request.user.is_anonymous:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(request.user, context={'request': request}).data)


@extend_schema(tags=["logout"])
class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="logout",
        responses={200: {}},
        examples=[OpenApiExample(name="Logout", value={"success": True})],
    )
    def list(self, request):
        logout(request)
        return Response({"success": True}, status=status.HTTP_200_OK)
