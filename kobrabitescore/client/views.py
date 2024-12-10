from rest_framework import viewsets

from drf_spectacular.utils import extend_schema

from client.access import PUTLESS_METHODS
from client.models import Client
from client.filters import ClientFilter
from client.serializers import ClientNestedSerializer, ClientSerializer


@extend_schema(tags=['clients'])
class ClientViewSet(viewsets.ModelViewSet):
    http_method_names = PUTLESS_METHODS
    queryset = Client.objects.order_by('first_name', 'last_name')
    serializer_class = ClientNestedSerializer
    list_serializer_class = ClientSerializer
    filterset_class = ClientFilter

    def get_queryset(self):
        qs = self.queryset
        return qs.prefetch_related('user')

    def get_serializer_class(self):
        if self.action in ['list']:
            if getattr(self, 'swagger_fake_view', False):
                return super().get_serializer_class()
            else:
                return getattr(self, 'list_serializer_class', super().get_serializer_class())
        return super().get_serializer_class()

