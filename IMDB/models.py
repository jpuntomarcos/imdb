from django.db import models
from rest_framework.exceptions import NotFound


class Category(models.Model):
    """
    Category/genre of a movie
    """
    name = models.CharField(max_length=100, unique=True)  # Category name

    @staticmethod
    def check_and_get(category_data):
        """
        Utility that checks if category names exist, otherwise raises NotFound exception
        :param category_data: list of Dicts containing "name" as key, value is string
        :return: queryset with category entities matching category names, empty list if input is None
        """

        if category_data is not None:

            # Get categories
            category_names = [category['name'] for category in category_data]
            categories = Category.objects.filter(name__in=category_names)

            # Check if all categories exist, raise error otherwise
            missing_categories = set(category_names) - set(categories.values_list('name', flat=True))
            if len(missing_categories) > 0:
                raise NotFound(f"The following categories do not exist: {', '.join(missing_categories)}")

            return categories

        else:
            return []


class Movie(models.Model):
    """
    Movie entity
    """
    title = models.TextField()  # Movie title
    imdb_tconst = models.CharField(max_length=20, unique=True, null=False, blank=False)  # The IMDB tconst ID
    year = models.PositiveSmallIntegerField(null=True)  # The year the movie was released
    runtime = models.PositiveSmallIntegerField(null=True)  # The runtime of the movie in minutes
    rating = models.FloatField(null=True)  # The rating of the movie on a scale of 0 to 10
    category = models.ManyToManyField(Category)  # The categories that the movie belongs to
