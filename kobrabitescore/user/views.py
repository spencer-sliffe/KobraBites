import logging

from django.contrib.auth import logout, login
from django.middleware.csrf import get_token
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from client.access import PUTLESS_METHODS
from user.serializers import UserSerializer, User, LoginSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["login"])
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = PUTLESS_METHODS
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return super().get_permissions()


@extend_schema(tags=["login"])
class LoginViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        operation_id="login",
        request=LoginSerializer,
        responses={
            201: UserSerializer,
            400: {}
        },
    )
    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # This sets the session cookie
        login(request, user)
        return Response(UserSerializer(instance=user, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id="get_current_user",
        responses={
            200: UserSerializer,
        }
    )
    def list(self, request):
        get_token(request)
        if request.user.is_anonymous:
            return Response({}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserSerializer(instance=request.user, context={'request': request}).data)


@extend_schema(tags=["login"])
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
