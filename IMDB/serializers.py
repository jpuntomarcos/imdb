from rest_framework import serializers

from IMDB.models import Movie, Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Category model
    """
    name = serializers.CharField()

    class Meta:
        model = Category
        fields = ['name']


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Movie model
    """
    category = CategorySerializer(many=True, required=True)
    link = serializers.SerializerMethodField()  # link to the movie's IMDB page

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'rating', 'runtime', 'imdb_tconst', 'link', 'category']
        read_only_fields = ['id', 'link']

    def get_link(self, obj):
        """
        Returns a link to the movie's IMDB page.
        :param obj: Movie instance
        :return: link to the movie's IMDB page
        """
        return f'https://www.imdb.com/title/{obj.imdb_tconst}/'

    def create(self, validated_data):
        """
        Creates a new Movie instance, given the validated data.
        :param validated_data: validated data sent
        :return: Movie instance
        """

        # Get related categories
        category_data = validated_data.pop('category')
        categories = Category.check_and_get(category_data)

        # Create Movie
        movie = Movie.objects.create(**validated_data)
        movie.category.set(categories)

        return movie

    def update(self, instance, validated_data):
        """
        Updates a new Movie instance, given the validated data.
        :param instance: Movie instance to be updated
        :param validated_data: validated data sent
        :return: updated Movie instance
        """

        # Update related categories
        category_data = validated_data.pop('category', None)
        categories = Category.check_and_get(category_data)
        instance.category.set(categories)

        # Update rest of instance
        super().update(instance, validated_data)

        return instance
