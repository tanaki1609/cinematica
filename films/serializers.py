from rest_framework import serializers
from .models import Film, Director


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
