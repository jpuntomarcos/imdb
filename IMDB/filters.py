import django_filters

from IMDB.models import Movie


class MovieFilter(django_filters.FilterSet):
    """
    Defines filters for Movie entity
    """
    # Filter for category name, allowing multiple values
    category__eq = django_filters.AllValuesMultipleFilter(field_name='category__name')

    # Filters for rating: exact, less and greater
    rating__eq = django_filters.NumberFilter(field_name='rating', label="Rating equal to")
    rating__lt = django_filters.NumberFilter(field_name='rating', lookup_expr='lt')
    rating__gt = django_filters.NumberFilter(field_name='rating', lookup_expr='gt')

    class Meta:
        model = Movie
        fields = []
