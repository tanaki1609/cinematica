from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id first_name last_name'.split()


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(many=False)
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id title rating created director genres'.split()
        # depth = 1

    def get_genres(self, film):
        return film.genre_names


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, min_length=2)
    text = serializers.CharField(default='No text')
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField()
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist!')
        return director_id

    def validate_genres(self, genres):  # [1,2,17]
        genres_from_db = Genre.objects.filter(id__in=genres)  # [1,2]
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres
