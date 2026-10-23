from rest_framework import serializers
from .models import Film


class FilmDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'


class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        # fields = ['id', 'title', 'release_year', 'rating', 'created']
        # fields = '__all__'
        # exclude = ['text', 'release_year', 'rating']
        fields = 'id title rating created'.split()
