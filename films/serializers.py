from rest_framework import serializers
from .models import Film, Director


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
