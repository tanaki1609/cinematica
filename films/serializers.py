from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id first_name last_name'.split()


class FilmListSerializer(serializers.ModelSerializer):
    director = DirectorSerializer()
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Film
        fields = 'id title rating is_hit created director genres reviews'.split()
        depth = 1

    def get_genres(self, film):
        return sorted(film.genre_names())


class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=1)
    text = serializers.CharField(required=False)
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField(default=True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField())

    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director not found!')
        return director_id

    def validate_genres(self, genres):  # [1,2,10]
        genres = list(set(genres))
        genres_from_db = Genre.objects.filter(id__in=genres)  # [1,2]
        if len(genres_from_db) != len(genres):
            raise ValidationError('Genre does not exist!')
        return genres
