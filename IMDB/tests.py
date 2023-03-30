from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Movie
from .serializers import MovieSerializer


class MovieTests(APITestCase):

    def setUp(self):
        """
        Initial Movie test setup
        """
        self.movies_url = reverse('movie-list')
        self.category = Category.objects.bulk_create([Category(name="Action"), Category(name="Sci-Fi")])
        self.movie_data = {
            'title': 'Die Hard',
            'imdb_tconst': 'tt0095016',
            'year': 1988,
            'runtime': 132,
            'rating': 8.2
        }

        # Get related categories
        categories = Category.check_and_get([{'name': 'Action'}])

        # create movie and set categories
        self.movie = Movie.objects.create(**self.movie_data)
        self.movie.category.set(categories)

        # Create serializer
        self.movie_serializer = MovieSerializer(instance=self.movie)

    def test_list_movies(self):
        """
        Tests listing of movies
        """
        response = self.client.get(self.movies_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"], [self.movie_serializer.data])

    def test_create_movie(self):
        """
        Ensure we can create a new account object.
        """

        # Input data
        new_movie_data = {
            'title': 'The Matrix',
            'imdb_tconst': 'tt0133093',
            'year': 1999,
            'runtime': 136,
            'rating': 8.7,
            'category': [{'name': 'Action'}, {'name': 'Sci-Fi'}],
        }

        # Create and assert
        response = self.client.post(self.movies_url, new_movie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)
        self.assertEqual(Movie.objects.last().category.count(), 2)
        self.assertEqual(Movie.objects.last().title, 'The Matrix')

    def test_update_movie(self):
        """
        Ensure we can update an existing movie object.
        """

        # Input data
        updated_movie_data = {
            'title': 'Die Hard 2',
            'year': 1990,
            'runtime': 124,
        }

        # Update and assert
        movie_id = self.movie.id
        response = self.client.patch(f'{self.movies_url}{movie_id}/', updated_movie_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Movie.objects.get(id=movie_id).title, 'Die Hard 2')
        self.assertEqual(Movie.objects.get(id=movie_id).year, 1990)
        self.assertEqual(Movie.objects.get(id=movie_id).runtime, 124)

    def test_filter_movies(self):
        """
        Ensure we can filter movies by category.
        """

        # Input data
        category_name = 'Action'

        # Filter and assert
        response = self.client.get(f'{self.movies_url}?category={category_name}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]['category'][0]['name'], 'Action')
