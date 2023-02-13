from django_filters import rest_framework as filters
from .models import Movie


# метод визначає ip адрес користувача
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    # за замовчуванням шукає по id , а ми будемо шукати по field_name='genres__name'
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    # діапазон дат - year_min=1212&year_max=2323
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
