import django_filters
from django.db.models import Prefetch
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets, filters
from django.conf import settings
from IMDB.filters import MovieFilter
from IMDB.models import Movie, Category
from IMDB.renderers import OnlyRawBrowsableAPIRenderer
from IMDB.serializers import MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint to list and manage movies
    """

    # Configure ViewSet:
    renderer_classes = [OnlyRawBrowsableAPIRenderer, JSONRenderer]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    ordering = ['title']  # default ordering
    # ordering_fields = ('year', 'rating', 'title')  # fields that can be used for ordering
    ordering_fields = '__all__'
    # ordering = ['{0}'.format(field) for field in ordering_fields] + ['id']
    filterset_class = MovieFilter  # Movie filtering options

    def get_queryset(self):
        """
        Overrides get_queryset to make it slightly more efficient by saving some queries
        :return:
        """
        queryset = super().get_queryset()

        # prefetch categories
        prefetch = Prefetch('category', queryset=Category.objects.all())
        queryset = queryset.prefetch_related(prefetch)

        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Post actions are restricted if ALLOW_POST_ACTIONS_TO_UNAUTHENTICATED_USERS is False
        """

        if not settings.ALLOW_POST_ACTIONS_TO_UNAUTHENTICATED_USERS \
                and self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
