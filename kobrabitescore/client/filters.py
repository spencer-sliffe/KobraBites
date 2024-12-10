import django_filters
from django.db.models import Q, F, Value
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models.functions import Concat
from client.models import Client


class ClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    order_by = django_filters.OrderingFilter(fields=(('full_name', 'full_name'),))

    def filter_search(self, queryset, name, value):
        queryset = queryset.annotate(
            full_name=Concat(F('first_name'), Value(' '), F('last_name'))
        )

        exact_name_queryset = queryset.filter(full_name__icontains=value)
        if exact_name_queryset.exists():
            return exact_name_queryset

        search_query = SearchQuery(value)
        search_vector = (
            SearchVector('first_name', weight='A') +
            SearchVector('last_name', weight='A') +
            SearchVector('user__email', weight='B')
        )

        ranked_queryset = queryset.annotate(
            rank=SearchRank(search_vector, search_query)
        ).filter(rank__gt=0).order_by('-rank')

        if not ranked_queryset.exists():
            return queryset.filter(
                Q(first_name__icontains=value) |
                Q(last_name__icontains=value) |
                Q(user__email__icontains=value)
            )

        return ranked_queryset

    class Meta:
        model = Client
        fields = ['id', 'search']
